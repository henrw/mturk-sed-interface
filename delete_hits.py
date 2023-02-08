import boto3
from datetime import datetime

# Get the MTurk client
mturk=boto3.client('mturk',
        region_name='us-east-1',
        endpoint_url="https://mturk-requester-sandbox.us-east-1.amazonaws.com",
    )

# Delete HITs
hits_id = [
    # TODO
]

for hit_id in hits_id:

    # Get HIT status
    status=mturk.get_hit(HITId=hit_id,)['HIT']['HITStatus']
    print('HITStatus:', status)

    # If HIT is active then set it to expire immediately
    if status=='Disposed':
        response = mturk.update_expiration_for_hit(
            HITId=hit_id,
            ExpireAt=datetime(2015, 1, 1)
        )        

    # Delete the HIT
    try:
        mturk.delete_hit(HITId=hit_id)
    except:
        print('Not deleted')
    else:
        print('Deleted')