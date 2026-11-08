# Python SMTP Mail Client

## Project Information

- **Project:** Python Lab 3 - SMTP Mail Client
- **Name:** Carlos Gutierrez
- **Email:** cgutierrez44833@ucumberlands.edu
- **Course:** MSCS-631-B01 Advanced Computer Networks

A small SMTP mail client written in Python using raw sockets (no `smtplib`). It connects over TCP and speaks SMTP step by step (`EHLO`, `AUTH`, `MAIL FROM`, `RCPT TO`, `DATA`, message body, `QUIT`), checks the reply code of every step, and sends one email.

## Usage

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```

Create a `.env` file in the project root:

```env
DEV=dev
USER_NAME=your_smtp_username
PASS=your_smtp_password
```

`DEV=dev` uses the local test server and skips the login step. `USER_NAME` and `PASS` are only used with a real server.

### Option 1: local test server (no account)

Install and start a local debugging SMTP server (keep it running):

```bash
pip install aiosmtpd
python3 -m aiosmtpd -n -l localhost:1025
```

In a second terminal, run the client:

```bash
python src/smtp.py
```

The server terminal prints the subject and body of the received message.

### Option 2: real mail server

1. Remove `DEV` from `.env`.
2. Fill in `USER_NAME` and `PASS`.
3. Set the sender and recipient in `src/smtp.py`.
4. Run the client:

```bash
python src/smtp.py
```

### Example output

```text
220 macbook-pro.local Python SMTP 1.4.6
EHLO Alice            -> 250 macbook-pro.local
MAIL FROM             -> 250 OK
RCPT TO               -> 250 OK
DATA                  -> 354 End data with <CR><LF>.<CR><LF>
\r\n.\r\n             -> 250 OK
QUIT                  -> 221 Bye
```

### Notes

- Every SMTP command ends in CRLF (`\r\n`), and the message body ends with `\r\n.\r\n` (`endmsg`).
- `EHLO` replies are multi-line, so the client reads until the final line.
- The client stops at the first unexpected reply code.
- Mail sent to a real provider can land in spam.
- Never commit `.env`.
