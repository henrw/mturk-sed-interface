import boto3
import pandas as pd
import meta
from agent.results.labels import AI_labels


session = boto3.Session()
client = session.client(
    service_name='mturk',
    region_name='us-east-1',
    endpoint_url=meta.mturk_environment['endpoint'],
)

# Test that you can connect to the API by checking your account balance
user_balance = client.get_account_balance()
print("Your account balance is {}".format(user_balance['AvailableBalance']))

# Set qualification
# qualification_id = None
# qualification_id = "3PHD6OHA9KR85JUB79QM4LWDFBH9WQ"
qualification_id = "38KPZWBG0L8VZAMW7H57M1G5AP38UG"

if qualification_id == "":
    questions = open('templates/qualification_questions.xml', mode='r').read()
    answers = open('templates/qualification_answers.xml', mode='r').read()

    qual_response = client.create_qualification_type(
                        Name='Hearing Assessment',
                        Keywords='test, qualification, hearing',
                        Description='This is a brief hearing test',
                        QualificationTypeStatus='Active',
                        Test=questions,
                        AnswerKey=answers,
                        TestDurationInSeconds=60*2)
    qualification_id = qual_response['QualificationType']['QualificationTypeId']
    print(qualification_id)
# Set hit
question_html = open("templates/index.html", 'r').read()
question_xml = f"""
    <HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
    <HTMLContent><![CDATA[{question_html}]]>
    </HTMLContent>
    <FrameHeight>800</FrameHeight>
    </HTMLQuestion>
"""

hit_params = {
    "MaxAssignments": 25,
    "LifetimeInSeconds": 60*60*24*30,
    "AssignmentDurationInSeconds": 60*20,
    "Reward": meta.mturk_environment['reward'],
    "Title": 'Audio Event',
    "Keywords": 'sound, audio, event, research',
    "Description": 'Describe the event(s) in the audio.',
    "QualificationRequirements": [] if qualification_id is None else [{'QualificationTypeId': qualification_id,
                                   'Comparator': 'GreaterThanOrEqualTo',
                                   'IntegerValues':[50]}],
}

# Create hits
hits = []
audio_df = pd.read_csv("data/dev.csv")
for id, row in audio_df.iterrows():
    file = row["file"]
    labels = [x.strip() for x in row["labels"].split(';')]
    question_xml_replaced = question_xml.replace(
        "${sed_img_url}",meta.s3_prefix+file.replace("wav","png")).replace(
        "${audio_url}", meta.s3_prefix+file).replace(
        "${img_url}", meta.s3_prefix+file.replace("sound","thumbnail").replace("wav","png")).replace(
        '["${suggested}"]', '['+','.join([f'\"{x}\"' for x in AI_labels[id+3]])+']')
    response = client.create_hit(
        **hit_params,
        Question = question_xml_replaced,
    )

    hit_type_id = response['HIT']['HITTypeId']
    hit_id = response['HIT']['HITId']
    hits.append(hit_id)

print("You can work the HIT here:")
url = meta.mturk_environment['preview'] + "?groupId={}".format(hit_type_id)
print(url)

print("And see results here:")
print(meta.mturk_environment['manage'])

with open("cache/hits.txt", "w") as f:
    f.writelines([hit+'\n' for hit in hits])

with open("cache/hits_worker.txt", "w") as f:
    f.write(url)
