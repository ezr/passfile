# passfile
Avoid leaving sensitive files on disk when they are not needed. Uses the "pass" password manager.

## An example use case
The aws-cli tool for Amazon Web Services saves its credentials in plain text in the user's home directory. Any program I use can read the file and get access to the Amazon account. I only occasionally use aws-cli. When I want to use aws-cli I run passfile once, it creates the credential file, and then deletes it again after a certain amount of time.

```
$ ls ~/.aws/
config 

$ ./passfile.py aws-credentials
successfully wrote to /home/gravel/.aws/credentials
added an atd job to delete /home/gravel/.aws/credentials in 600 minutes

$ ls ~/.aws
config  credentials

$ cat ~/.aws/credentials
[default]
aws_access_key_id = udHVoc3JjcmFjZ2NvZ3J
aws_secret_access_key = dWhzYWNvZWh1c2xhcmNvZWh1YXJvZWN1aGxhcmNY

[otheruser]
aws_access_key_id = HVsYXJjb2VodWxhcmNbb
aws_secret_access_key = dWxhN2QgYXNub3RlaHVzYXRvZXVsOWE4Z2Z1bDc5
region = us-east-2
```

## Requirements
- python 3: https://www.python.org/
- pass: https://www.passwordstore.org/
- at daemon: http://blog.calhariz.com/tag/at

## Configuration
Configure pass as described at https://www.passwordstore.org/. For each text file used by passfile, save the data in pass under a 'files' directory. The first line in the file saved by pass should be the path to the file when written on disk. The rest of the file saved by pass should be the contents of the file that will be written. So this is what I get when I run 'pass files/aws-credentials' (the keys shown here are faked):
```
$ pass files/aws-credentials 
/home/ezr/.aws/credentials
[default]
aws_access_key_id = udHVoc3JjcmFjZ2NvZ3J
aws_secret_access_key = dWhzYWNvZWh1c2xhcmNvZWh1YXJvZWN1aGxhcmNY

[otheruser]
aws_access_key_id = HVsYXJjb2VodWxhcmNbb
aws_secret_access_key = dWxhN2QgYXNub3RlaHVzYXRvZXVsOWE4Z2Z1bDc5
region = us-east-2
```
For binary files, we base64 encode the data saved by pass. The second line in the file is "binary". The tobase64 script outputs the info to save in pass for binary files.
```
$ pass files/gcloud-creds  | head
/home/ezr/.config/gcloud/credentials.db
binary
3Rq4HfWLEbVwmGETbaybArkFJKWIUGyO0BiVyKhA++Qxkg8EoidXLT42gfDi0sW9xSjkqiIlmWS3
6Z+gm7nl6VxkM/nS2Zhf+V7Ntk1KXuhy4jExaonTI7JX0307MFywedRboFMs3M1GlMLr+6WenSig
```

To enable bash completion, you can add this to your bashrc:
```
complete -W "$(ls $HOME/.password-store/files/  | rev | cut --complement -f 1 -d '.' | rev)" passfile.py
```
