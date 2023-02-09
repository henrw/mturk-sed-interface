import boto3
import xmltodict
import csv
import meta
from os import path

hit_file = 'cache/hits.txt'
out_file = 'results/assignments.csv'

hits = [x.strip() for x in open(hit_file).readlines()]
print(hits)

client = boto3.client(
    service_name='mturk',
    region_name='us-east-1',
    endpoint_url=meta.mturk_environment['endpoint'],
)

write_header = False
if not path.exists(out_file): 
    write_header = True

with open(out_file, 'a', newline='') as csvfile:
    fieldnames = ['AssignmentId', 'WorkerId', 'HITId', 'AutoApprovalTime', 'AcceptTime', 'SubmitTime', 'Answer', 'IsHint']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if(write_header): writer.writeheader()

    for hit_id in hits:
        
        # Get the status of the HIT
        hit = client.get_hit(HITId=hit_id)
        status = hit['HIT']['HITStatus']
        # Get a list of the Assignments that have been submitted
        assignmentsList = client.list_assignments_for_hit(
            HITId=hit_id,
            AssignmentStatuses=['Submitted', 'Approved'],
        )
        assignments = assignmentsList['Assignments']
        assignments_submitted_count = len(assignments)
        answers = []
        for assignment in assignments:
        
            # Retreive the attributes for each Assignment
            worker_id = assignment['WorkerId']
            assignment_id = assignment['AssignmentId']
            
            # Retrieve the value submitted by the Worker from the XML
            answer_dict = xmltodict.parse(assignment['Answer'])

            answer = answer_dict['QuestionFormAnswers']['Answer'][0]['FreeText']
            is_hint = answer_dict['QuestionFormAnswers']['Answer'][1]['FreeText']
            
            # Approve the Assignment (if it hasn't been already)
            if assignment['AssignmentStatus'] == 'Submitted':
                client.approve_assignment(
                    AssignmentId=assignment_id,
                    OverrideRejection=False
                )

                writer.writerow({'AssignmentId': assignment['AssignmentId'], 
                                'WorkerId': assignment['WorkerId'], 
                                'HITId': assignment['HITId'],  
                                'AutoApprovalTime': assignment['AutoApprovalTime'],  
                                'AcceptTime': assignment['AcceptTime'],  
                                'SubmitTime': assignment['SubmitTime'],  
                                'Answer': answer,
                                'IsHint': is_hint})