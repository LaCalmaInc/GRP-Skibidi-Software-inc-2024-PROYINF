## Inspección de Código con SonarQube

### Issue 1
![Issue1](https://github.com/LaCalmaInc/GRP-Skibidi-Software-inc-2024-PROYINF/blob/main/inspections/issue1.png)



### Issue 2
![Issue2](https://github.com/LaCalmaInc/GRP-Skibidi-Software-inc-2024-PROYINF/blob/main/inspections/issue2.png)

In most cases, trust boundaries are violated when a secret is exposed in a source code repository or an uncontrolled deployment environment. Unintended people who don’t need to know the secret might get access to it. They might then be able to use it to gain unwanted access to associated services or resources.

The trust issue can be more or less severe depending on the people’s role and entitlement.

What is the potential impact?
If a Django secret key leaks to an unintended audience, it can have serious security implications for the corresponding application. The secret key is used to sign cookies and other sensitive data so that an attacker could potentially use it to perform malicious actions.

For example, an attacker could use the secret key to create their own cookies that appear to be legitimate, allowing them to bypass authentication and gain access to sensitive data or functionality.

In the worst-case scenario, an attacker could be able to execute arbitrary code on the application and take over its hosting server. 
Revoke the secret

Revoke any leaked secrets and remove them from the application source code.

Before revoking the secret, ensure that no other applications or processes are using it. Other usages of the secret will also be impacted when the secret is revoked.

In Django, changing the secret value is sufficient to invalidate any data that it protected. It is important to not add the revoked secret to the SECRET_KEY_FALLBACKS list. Doing so would not prevent previously protected data from being used.

Use a secret vault

A secret vault should be used to generate and store the new secret. This will ensure the secret’s security and prevent any further unexpected disclosure.

Depending on the development platform and the leaked secret type, multiple solutions are currently available.

Noncompliant code example
SECRET_KEY = 'r&lvybzry1k+qq)=x-!=0yd5l5#1gxzk!82@ru25ntos3_9^'
Compliant solution
import os

SECRET_KEY = os.environ["SECRET_KEY"]
