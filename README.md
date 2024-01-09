# ChittyBot

Simple context aware chat bot that can carry a conversation with a human.
Built with LangChain, Streamlit and AWS Bedrock.

## Setup

### Dev Environment

1. Setup Python 3.11 virtual environment. I used Anaconda to create mine. Install required dependences afterwards.
    ```bash
    conda create -n py3.11 python=3.11

    pip install streamlit
    pip install langchain
    pip install python-dotenv
    pip install boto3>=1.33.13
    ```
    
2. Create `.env` file and add AWS environment variables required by `boto3`
    ```bash
    AWS_DEFAULT_PROFILE=<your-aws-profile>
    AWS_DEFAULT_REGION=<your-aws-region>
    ```

3. Setup VS Code Debugging
    ```json
    {
      "version": "0.2.0",
      "configurations": [
        {
          "name": "Debug Streamlit App",
          "type": "python",
          "request": "launch",
          "program": "/path/to/streamlit/executable/py3.11/bin/streamlit",
          "args": [
            "run",
            "<my_app_code>.py"
          ],
          "console": "integratedTerminal",
          "justMyCode": true
        }
      ]
    }
    ```
    

### AWS Credentials

The following are required before we can successfully invoke a Bedrock model:

- Ensure you have [requested access to the models](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)
- IAM role granted with permissions to invoke specific Bedrock models
- Add trust policy to allow our IAM user to assume the IAM role

#### Steps
1. If you do not have an IAM role yet, create one and add the following policies. We will assume this role with our AWS identity to invoke Bedrock models. Model IDs can be found in the [AWS Docs](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-reference.html).

    
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
    				{
                "Sid": "BedrockInvokeModel",
                "Effect": "Allow",
                "Action": [
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream"
                ],
                "Resource": [
                    "arn:aws:bedrock:<aws-region>::foundation-model/anthropic.claude-v2",
                    "arn:aws:bedrock:<aws-region>::foundation-model/amazon.titan-embed-text-v1"
                ]
            },
            {
                "Sid": "ReadPermsAndXRay",
                "Effect": "Allow",
                "Action": [
                    "bedrock:ListFoundationModels",
                    "xray:PutTelemetryRecords",
                    "xray:PutTraceSegments"
                ],
                "Resource": "*"
            }
        ]
    }
    ```
    

2. Add a trust policy to the role you just created to allow your user to assume that role
    
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com",
                    "AWS": "arn:aws:iam::<aws-acct-no>:user/<aws-user-for-your-profile>"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    ```
    

3. Configure role we will assume locally. Add the following to your `~/.aws/config` file. `boto3` which LangChain uses to connect to AWS, will pick up this configuration and assume the correct identity.
    
    ```toml
    [profile <whatever-profile-name-you-like]
    role_arn=arn:aws:iam::<aws-account-number>:role/<iam-role-to-assume>
    source_profile=<your-aws-profile> # must be a valid aws profile from ~/.aws/credentials
    ```

## Run Streamlit Locally
To run the web application, execute: `streamlit run langchain_streamlit_awsbr.py`.
This will automatically open a page in your browser and direct you to `http://localhost:8502`.

To kill/stop the app, simply type `CTRL + C` in the terminal.