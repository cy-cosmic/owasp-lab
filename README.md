## OWASP Security Labs


 


A hands-on collection of intentionally vulnerable web applications demonstrating real-world security flaws from the OWASP Top 10.

Each lab simulates realistic developer mistakes and shows how attackers identify, exploit, and understand vulnerabilities commonly found in production systems.

The focus is practical skill-building for:

- penetration testing
- bug bounty hunting
- secure software development
- security engineering interviews
- understanding attacker mindset
#### Live demo

------
Explore the labs: [https://owasp.cyprian.dev](https://owasp.cyprian.dev)

Each vulnerability includes:

- explanation of the security flaw
- interactive vulnerable implementation
- guided exploitation walkthrough
- secure coding approach
#### Tech Stack

---
- Python
- Django
- Bootstrap (dark mode UI)
- PostgreSQL
- HTML / CSS / JavaScript
- Linux deployment environment
- Nginx + Gunicorn
- Git version control

### Implemented OWASP Top 10 Labs

---
#### A01. Broken Access Control - Insecure Direct Object Reference (IDOR)

Demonstrates how predictable object identifiers allow attackers to access resources belonging to other users when authorization checks are missing.

##### *Concepts covered:*

- object-level authorization
- horizontal privilege escalation
- multi-tenant data isolation
- secure query filtering by session ownership
#### A02. Cryptographic Failures - Privilege Escalation via Exposed Signing Key

Shows how exposed cryptographic secrets allow attackers to forge trusted cookies and escalate privileges.

##### *Concepts covered:*

- cookie signing
- integrity vs confidentiality
- secret key exposure in repositories
- client-side trust vulnerabilities
- 
#### A03. Injection - SQL Injection

Demonstrates how unsanitized input can allow attackers to manipulate database queries and access unauthorized data.

##### *Concepts covered:*

- unsafe query construction
- authentication bypass
- data exfiltration
- parameterized queries
- ORM protections
### Project Structure

___

    |owasp-lab/
        ├─── labs/
        ├────── migrations/
        ├─── owasp_lab/
        ├─── polls/
        ├────── fixtures/
        ├────── migrations/
        ├─── static/
        ├─── templates/
        ├────── labs/
        ├────── polls/
        ├── manage.py
        ├── README.md
        ├── requirements

Each lab contains:

- vulnerable implementation
- exploitation walkthrough
- secure implementation example
- reproducible attack scenario
### Learning Methodology

---

Each vulnerability is explored in three stages:

#### *Vulnerable implementation*

Demonstrates insecure coding patterns frequently found in real applications.

#### *Exploitation walkthrough*

Shows how attackers identify weaknesses and manipulate application behavior.

#### *Secure implementation*

Demonstrates defensive coding practices that prevent exploitation.

### Why this project is useful

---

Many resources explain vulnerabilities theoretically but do not demonstrate how they are exploited in practice.

This project emphasizes:

- realistic attack scenarios
- developer mistakes commonly found in production
- practical understanding of web security risks
- building intuition for secure design decisions

The labs simulate common issues such as:

- trusting client-side data
- weak access control enforcement
- exposed cryptographic secrets
- unsafe database queries
### Running locally

---

Clone repository:

``` git clone https://github.com/yourusername/owasp-labs.git```

Enter project directory:

```cd owasp-labs```

Create virtual and activate environment:

```bash
  python3 -m venv venv && source venv/bin/activate
 ```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run development server:

```bash
python manage.py runserver
```

Access labs:

http://127.0.0.1:8000/labs/

### Disclaimer

---

* These labs intentionally include security vulnerabilities for educational purposes.

* Do not deploy vulnerable configurations in production environments.

* Use responsibly and only in controlled testing environments.

### Roadmap

---

#### Planned additions:

* Cross-Site Scripting (XSS)
* Cross-Site Request Forgery (CSRF)
* Security Misconfiguration
* Identification and Authentication Failures
* Server-Side Request Forgery (SSRF)

### Author

---

#### Cyprian Munene - Python Developer | Security Engineer

*Portfolio:* https://cyprian.dev

*Live Project:* https://owasp.cyprian.dev