# ChittyBot

Simple context aware chat bot that can carry a conversation with a human.
Built with LangChain, Streamlit and AWS Bedrock.

## Setup

### Dev Environment

1. I used a Python 3.11 environment. You can use virtual environments like `conda` or `venv`. Install the following dependencies in your Python environment.
    - `pip install streamlit`
    - `pip install langchain`
    - `pip install python-dotenv`
    - `pip install boto3>=1.33.13`
    
2. In your project folder, create a `.env` file and add the following key/value pairs. Ensure the values provided match your AWS credentials.
    
    ```bash
    AWS_DEFAULT_PROFILE=<your-aws-profile>
    AWS_DEFAULT_REGION=<your-aws-region>
    ```
    

1. If you are using VS Code and need to debug or step through code, create a debug configuration with the following details.
    
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
                    "arn:aws:bedrock:<aws-region>::foundation-model/anthropic.claude-v2:1",
                    "arn:aws:bedrock:<aws-region>::foundation-model/anthropic.claude-instant-v1",
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
    
    ```text
    [profile <whatever-profile-name-you-like]
    role_arn=arn:aws:iam::<aws-account-number>:role/<iam-role-to-assume>
    source_profile=<your-aws-profile> # must be a valid aws profile from ~/.aws/credentials
    ```

## Run Streamlit Locally
To run the web application, execute: `streamlit run <your_code_file.py>`.
This will automatically open a page in your browser and direct you to `http://localhost:8502`.

To kill/stop the app, simply type `CTRL + C` in the terminal.
