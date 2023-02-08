s3_prefix = "https://sound-events.s3.amazonaws.com/"

create_hits_in_live = False

environments = {
    "live": {
        "endpoint": "https://mturk-requester.us-east-1.amazonaws.com",
        "preview": "https://www.mturk.com/mturk/preview",
        "manage": "https://requester.mturk.com/mturk/manageHITs",
        "reward": "0.00"
    },
    "sandbox": {
        "endpoint": "https://mturk-requester-sandbox.us-east-1.amazonaws.com",
        "preview": "https://workersandbox.mturk.com/mturk/preview",
        "manage": "https://requestersandbox.mturk.com/mturk/manageHITs",
        "reward": "0.10"
    },
}

mturk_environment = environments["live"] if create_hits_in_live else environments["sandbox"]