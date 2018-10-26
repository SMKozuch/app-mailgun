## Mailgun

Mailgun component is able to send an email via Mailgun API. 
Basic requirements are:
  * Mailgun account
  * registered domain (if emails are to be sent outside of sandbox accepted; see Mailgun help)

This component takes as input a table of email addresses and names, to which an email is sent. In the table, other attributes can be added, which can then be used to fill in the html body (e.g. date of birth, etc.). **The input table needs to contain following columns: email, name, html_file, subject, attachments, delivery.**

### Inputs
Mailgun component takes the following parameters and table as inputs.

* **Username** - Mailgun username. If API key is used, fill in `api`. 
* **Token** - Password or API key for Mailgun.
* **Domain** - Domain, from which the mail should be sent. See [How to send mail](https://documentation.mailgun.com/en/latest/quickstart-sending.html#how-to-start-sending-email)
* **From** - Specifiec in whose name should the mail be sent.
* **Table** with records of emails, **with following columns**:
    * `email` - Email address to which an email will be sent.
    * `name` - Name of the person. Will be used in creating an email handle. Can be left blank.
    * `html_file` - Name of the file in KBC storage to be used as html body, in format `KBCID_filename.ext`, where `KBCID` is ID of the file in KBC storage, `filename.ext` is the name and extension of given file.
    * `subject` - Subject of an email.
    * `attachments` - String separated names of files in KBC storage to be attached to the email. Error is raised, if files are not inputted correctly or are not in the folder. Attachments must be in format `KBCID_filename.ext`, where `KBCID` is ID of the file in KBC storage, `filename.ext` is the name and extension of given file.
    * `delivery` - Scheduled delivery time in format `HH:MM:SS +ZZZZ` (e.g. `16:00:00 +0000`). If inputted correctly, an email will be delivered at this time. Otherwise, an email will be delivered straightaway.
    * `**kwargs` - Other columns. Each of these columns can be used to fill in the html body using standard Python string handlers. For example, if the html body has `Weather is %(weather)s, %(name)s.` in it, the handles `%(weather)s` and `%(name)s` will be replaced by their respective values in column `weather` and `name` from the input table, thus producing (e.g.) `Weather is nice, John.`


### Output
Message with information, whether a file was sent. See [Mailgun Logs](https://github.com/SMKozuch/app-mailgun-logs) application to obtain logs for sent emails.