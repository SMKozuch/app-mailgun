## Mailgun

Mailgun component is able to send an email via Mailgun API. 
Basic requirements are:
  * Mailgun account
  * registered domain (if emails are to be sent outside of sandbox; see Mailgun help)

This component takes as input a table of email addresses and names, to which an email is sent. In the table, other attributes can be added, which can then be used to fill in the html body (e.g. date of birth, etc.). **The table needs to contain columns *email* and *name*, that are used to create recipient ID.**

### Inputs
Mailgun component takes the following parameters as inputs.

* **username** - Mailgun username. If API key is used, fill in `api`. 
* **Token** - password or API key for Mailgun.
* **Mailing list name** - the name of the table, used as an input, which contains e-mail addresses, names and other related attributes. Full file name needs to be specified, including the .csv extension.
* **HTML Body** - storage name of the .html file, that is used as an email body. The name of the file needs to be provided as `ID_name.html`, where `ID` is Keboola Storage ID, and `name` is the name of the file. The file can be filled with recipients details, using standard python `%(name_of_column)s` code. The whole piece of code is replaced by the value from the input table, from column specified instead of `name_of_column`. As an example, `"Hello %(name)s from %(city)s"`, will produce `"Hello John from London", where both *John* and *London* are taken from the input table, from columns *name* and *city* respectively. 
* **From** - specified in whose name should the mail be sent. The parameter has to be provided in the form of `John Doe <john.doe@example.com>`, where `example.com` should be replaced by domain name. See Mailgun documentation for more help.
* **Subject** - subject of emails to be sent
* **Domain URL** - URL of the domain used. See Mailgun API help for more information.
* **Scheduled delivery time** - the time, when emails should be delivered.
* **Attachments** - An array of files to be sent as attachments. Filenames must be provided as 'ID_name.ext', where ID is Keboola Storage ID, name is the name of the file and ext its extension.


### Output
Information whether an email to specified email address was sent or not.
