import boto3
from datetime import datetime

# Get the MTurk client
mturk=boto3.client('mturk',
        region_name='us-east-1',
        endpoint_url="https://mturk-requester-sandbox.us-east-1.amazonaws.com",
    )

# Delete HITs
hits_id = [
    "391JB9X40BS3VGXHGSU69MN4FG0KM8",
    "3CRWSLD92XOML7IWEKMZG34DZLAMOU",
    "3J6BHNX0VMC9DYIHST96M1C4K6AKN8",
    "3OWZNK3RZY9RR8Y00OFO00I4B2HU2O",
    "34XASH8KM36467UXTKZE53939Q6MPB",
    "3OYHVNTV66IRVJITT89J1QC9AGFKON",
    "3OB6JN3AA39PIKAC6C33AY9IA8URM8",
    "3GKAWYFRB2D12DOKGR0BMDM90CEPDW",
    "3ABAOCJ4SLOP6JVCTXE358ZDEMSMQ2",
    "3126F2F5GLN6UJ2KCMBVSV4U0OFPEP",
    "3YGYP1365ETV02VCIDI3NDYIFY4RN8",
    "38LRF35D6YGGCQUJ4OTTJANWHGHU3Z",
    "3OB6JN3AA39PIKAC6C33AY9IA8UMR3",
    "3YGE63DIOLHXN2KRG1QBZ0AMZK8W05",
    "3JYPJ2TAZVSY0X2G7XV1ADPUCPUPF7",
    "3O71U79SSO91JZAPL13808EEWADMSR",
    "3FHTJGYT90K4EXYBIH1JSYP6D4UPG6",
    "338431Z1GYZDINVOJSIG22YN589RON",
    "3FTID4TN9YIE934DKVUIIHNQDQJYLF",
    "3K2CEDRADOL2YZN4A18YADA0YTRMTG",
    "3X2YVV51Q7OXUR59CKUBD5TW4CEW18",
    "3YLTXLH3ESQIETTM2NJ1DY17S47PH5",
    "3FDWKV9VD0MHYC2TA6Y8F9W2H7YMU7",
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