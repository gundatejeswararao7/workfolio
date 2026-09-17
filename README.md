# 💼 Workfolio — Professional Social Network & Work Marketplace

> **A unified professional social network and work marketplace built around one account, one profile, and multiple work contexts — connecting people, opportunities, communication, project execution, and professional reputation in one platform.**

<p align="center">

<img src="https://img.shields.io/badge/FRONTEND-555555?style=flat-square" />
<img src="https://img.shields.io/badge/REACT-61DAFB?style=flat-square&logo=react&logoColor=black" />
<img src="https://img.shields.io/badge/TYPESCRIPT-3178C6?style=flat-square&logo=typescript&logoColor=white" />
<img src="https://img.shields.io/badge/VITE-646CFF?style=flat-square&logo=vite&logoColor=white" />
<img src="https://img.shields.io/badge/TAILWIND_CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" />

<img src="https://img.shields.io/badge/BACKEND-555555?style=flat-square" />
<img src="https://img.shields.io/badge/PYTHON-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/FASTAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/PYDANTIC-E92063?style=flat-square&logo=pydantic&logoColor=white" />

<img src="https://img.shields.io/badge/DATABASE-555555?style=flat-square" />
<img src="https://img.shields.io/badge/SQLITE-003B57?style=flat-square&logo=sqlite&logoColor=white" />
<img src="https://img.shields.io/badge/SQLALCHEMY-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white" />

<img src="https://img.shields.io/badge/AUTHENTICATION-555555?style=flat-square" />
<img src="https://img.shields.io/badge/GMAIL_ONLY-EA4335?style=flat-square&logo=gmail&logoColor=white" />
<img src="https://img.shields.io/badge/OTP-3498DB?style=flat-square" />
<img src="https://img.shields.io/badge/SECURE_SESSIONS-8E44AD?style=flat-square" />

<img src="https://img.shields.io/badge/DEVELOPMENT-555555?style=flat-square" />
<img src="https://img.shields.io/badge/GIT-F05032?style=flat-square&logo=git&logoColor=white" />
<img src="https://img.shields.io/badge/GITHUB-181717?style=flat-square&logo=github&logoColor=white" />

</p>

<p align="center">
<img src="https://img.shields.io/badge/💼_PROFESSIONAL_NETWORK-UNIFIED_PROFILE-2563EB?style=for-the-badge" />
<img src="https://img.shields.io/badge/🤝_WORK_MARKETPLACE-PROJECTS-059669?style=for-the-badge" />
<img src="https://img.shields.io/badge/💬_SOCIAL_FEED-COMMUNICATION-7C3AED?style=for-the-badge" />
</p>

---

# 📌 Overview

**Workfolio** is a unified professional social network and work marketplace designed around a simple idea:

> **One account. One profile. Multiple ways to work.**

Instead of forcing users to switch between separate dashboards or roles, Workfolio allows the same user to participate in different professional contexts from a single account.

A person can:

* 👤 Build a professional profile
* 📝 Publish posts
* 💼 Create work opportunities
* 🔎 Discover opportunities
* 📩 Apply for work
* 💬 Communicate with other users
* 📋 Manage active projects
* 🔄 Request and handle revisions
* ⭐ Build professional reputation
* 💰 Use an internal demo wallet
* 🔔 Receive backend-generated notifications
* 🤖 Interact with an AI assistant
* 🏠 Return to the professional feed without changing accounts

The application combines **social networking, freelancing/work marketplace features, project management, communication, reputation, and an AI assistant** into one platform.

---

# 🎯 Project Objectives

The main objectives of Workfolio are:

* Provide one unified account for multiple professional activities.
* Connect people with work opportunities.
* Allow users to both **publish opportunities and apply for work**.
* Provide a professional social feed for networking and content sharing.
* Support communication between users.
* Manage projects from application to completion.
* Track deadlines and overdue work.
* Support explicit revision and resubmission workflows.
* Maintain professional reputation through reviews.
* Provide a safe internal demo wallet for project transactions.
* Generate notifications for important system events.
* Provide an AI assistant for database-backed professional actions.
* Keep irreversible actions under explicit user control.

---

# ✨ Key Features

## 👤 Unified Professional Profile

Workfolio uses a single user model rather than creating separate accounts for different professional roles.

A user can act as:

```text
                 ┌──────────────────┐
                 │      USER        │
                 └────────┬─────────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
      Publish Work    Apply for Work   Social Feed
            │             │             │
            ▼             ▼             ▼
        Requester      Assignee      Professional
                                      Network
```

The same account can move between these contexts without logging out or changing dashboards.

---

## 📧 Gmail-Only Registration

Workfolio restricts registration and password reset to **Gmail addresses**.

```text
User Registration
        ↓
Enter Gmail Address
        ↓
Generate OTP
        ↓
OTP Verification
        ↓
Create Account
        ↓
Professional Profile
```

Security rules include:

* 📧 Gmail-only email addresses
* 🔢 OTP-based verification
* ⏱️ OTP expiration
* 🚦 Attempt limiting
* 🔄 OTP resend controls
* 🔐 Secure password hashing
* 🛡️ Signed authentication sessions

During development, OTP values can be returned in the registration response and logged to the backend console.

When SMTP is configured, OTPs can be delivered through email.

---

# 🔐 Authentication & Session Security

Passwords are securely hashed before being stored.

```text
Password
   ↓
Secure Password Hashing
   ↓
Password Hash
   ↓
SQLite Database
```

Authentication uses signed sessions to maintain the user's logged-in state.

Plaintext passwords are not stored in the database.

---

# 📰 Professional Social Feed

Workfolio provides a professional feed where users can publish and interact with professional content.

```text
User
 │
 ▼
Create Post
 │
 ▼
Professional Feed
 │
 ├── Discover Content
 ├── Follow Professional Activity
 └── Return to Work Context
```

The feed is integrated into the same application instead of being separated into another product or dashboard.

---

# 💼 Work Opportunities

Users can publish opportunities directly from their account.

```text
Create Opportunity
        ↓
Add Work Details
        ↓
Publish Opportunity
        ↓
Other Users Discover It
        ↓
Applications
```

An opportunity can become the starting point for a complete work lifecycle.

---

# 📩 Applications

Users can apply for available opportunities.

```text
Opportunity
     ↓
View Details
     ↓
Apply
     ↓
Application Created
     ↓
Requester Reviews
     ↓
Accept / Reject
```

The application process connects the professional social side of Workfolio with its work marketplace.

---

# 🤝 Unified Work Context

Workfolio does not require separate requester and worker accounts.

Instead:

```text
                    ONE ACCOUNT
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
       Publish Work           Apply for Work
             │                     │
             ▼                     ▼
        Requester               Assignee
             │                     │
             └──────────┬──────────┘
                        ▼
                  Active Project
```

This allows users to create opportunities while also working on opportunities created by others.

---

# 📋 Project & Work Lifecycle

Once an application is accepted, the work enters an active state.

```text
Opportunity
     ↓
Application
     ↓
Accepted
     ↓
Active Work
     ↓
Submission
     ↓
Review
     │
     ├──────────────► Revision Required
     │                       │
     │                       ▼
     │                  Resubmission
     │                       │
     │                       ▼
     └──────────────────► Review
                             │
                             ▼
                         Completed
```

Work state transitions are handled explicitly by the backend.

---

# ⏰ Server-Side Deadlines

Work deadlines are calculated by the backend using:

```text
accepted_at
     +
configured duration
     ↓
deadline
```

The server determines the deadline rather than relying on client-side calculations.

If active work passes its deadline:

```text
Active Work
     ↓
Deadline Passed
     ↓
Overdue
```

Expired active work becomes **overdue** without being deleted or automatically reassigned.

---

# 🔄 Revision & Resubmission

Workfolio supports explicit revision workflows.

```text
Submitted
    ↓
Review
    ↓
┌───────────────┐
│               │
▼               ▼
Approved     Revision
               ↓
          Resubmission
               ↓
             Review
               ↓
           Completion
```

This provides a clear project lifecycle instead of treating every submission as automatically complete.

---

# 💰 Internal Demo Wallet

Workfolio includes an internal wallet system for demonstrating project transactions.

> ⚠️ **No real money or external payment gateway is used.**

The completion flow can be represented as:

```text
Project Completed
       ↓
Transaction Created
       ↓
Requester Wallet Debited
       ↓
Assignee Wallet Credited
       ↓
Transaction Completed
```

Wallet operations are performed atomically by the backend.

---

# 🔔 Backend Notifications

Important system events generate backend notifications.

Examples include:

* 📩 New applications
* ✅ Application decisions
* 💼 Work acceptance
* ⏰ Deadline-related events
* 🔄 Revision requests
* 📤 Resubmissions
* 🎉 Project completion
* 💰 Wallet transactions
* ⭐ Reviews
* 💬 Relevant communication events

```text
Backend Event
      ↓
Notification Created
      ↓
User Notification Center
      ↓
User Reads Notification
```

---

# 💬 Communication

Workfolio provides communication features that allow users to interact during their professional activities.

```text
User 1
  │
  ▼
Message
  │
  ▼
Backend
  │
  ▼
User 2
```

Communication is integrated into the same workspace so users do not need to leave the application to coordinate work.

---

# 🤖 AI Assistant

Workfolio includes an AI assistant designed to help users navigate professional activities.

The assistant can route requests related to:

```text
                  AI Assistant
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
      People      Opportunities     Deadlines
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                Database Actions
```

The assistant works with database-backed actions for areas such as:

* 👥 People
* 💼 Opportunities
* ⏰ Deadlines
* 📝 General professional requests

### Safety principle

The AI assistant **does not automatically perform irreversible actions**.

Important actions remain under explicit user control.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────────┐
                         │       Workfolio         │
                         │      React + Vite       │
                         │    TypeScript + Tailwind│
                         └────────────┬────────────┘
                                      │
                                      │ HTTP / REST
                                      ▼
                         ┌─────────────────────────┐
                         │      FastAPI Server     │
                         │                         │
                         │ Authentication          │
                         │ Users / Profiles        │
                         │ Posts                    │
                         │ Opportunities            │
                         │ Applications             │
                         │ Projects                 │
                         │ Messages                │
                         │ Notifications            │
                         │ Wallet                   │
                         │ Reviews                  │
                         │ AI Assistant             │
                         └────────────┬────────────┘
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
              ┌────────────────────┐    ┌────────────────────┐
              │ SQLite Database    │    │ Gmail SMTP         │
              │                    │    │                    │
              │ Users              │    │ OTP Delivery       │
              │ Profiles           │    │ Email Services     │
              │ Posts              │    └────────────────────┘
              │ Opportunities      │
              │ Applications       │
              │ Projects           │
              │ Messages           │
              │ Notifications      │
              │ Wallet Entries     │
              │ Reviews            │
              └────────────────────┘
```

---

# 🔄 Complete Application Workflow

```text
                         ┌──────────────┐
                         │   Register   │
                         └──────┬───────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │ Gmail OTP Verify   │
                     └─────────┬──────────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │ Create Account     │
                     └─────────┬──────────┘
                               │
                               ▼
                         ┌────────────┐
                         │   Login    │
                         └─────┬──────┘
                               │
                               ▼
                     ┌────────────────────┐
                     │ Professional       │
                     │ Profile            │
                     └─────────┬──────────┘
                               │
                ┌──────────────┼───────────────┐
                ▼              ▼               ▼
           Social Feed    Publish Work     Find Work
                │              │               │
                │              ▼               ▼
                │         Opportunity     Application
                │              │               │
                │              └───────┬───────┘
                │                      ▼
                │                Application
                │                      │
                │                      ▼
                │                  Accepted
                │                      │
                │                      ▼
                │                Active Work
                │                      │
                │                      ▼
                │                 Submission
                │                      │
                │              ┌───────┴────────┐
                │              ▼                ▼
                │          Revision          Approved
                │              │                │
                │              ▼                ▼
                │        Resubmission       Completed
                │                               │
                │                               ▼
                │                         Wallet Transfer
                │                               │
                └───────────────────────────────┘
```

---

# 🔄 Work Data Flow

```text
User
 ↓
Opportunity
 ↓
Application
 ↓
Acceptance
 ↓
Deadline Calculation
 ↓
Active Project
 ↓
Submission
 ↓
Review
 ↓
Revision / Approval
 ↓
Completion
 ↓
Wallet Transaction
 ↓
Review & Reputation
```

---

# 🧭 Work State Management

Workfolio uses explicit backend state transitions.

```text
┌────────────┐
│ Opportunity│
└─────┬──────┘
      ▼
┌────────────┐
│ Application│
└─────┬──────┘
      ▼
┌────────────┐
│  Accepted  │
└─────┬──────┘
      ▼
┌────────────┐
│   Active   │
└─────┬──────┘
      │
      ├───────────────► Overdue
      │
      ▼
┌────────────┐
│ Submitted  │
└─────┬──────┘
      │
      ├───────────────► Revision Required
      │                       │
      │                       ▼
      │                  Resubmitted
      │                       │
      └───────────────────────┘
              │
              ▼
         ┌──────────┐
         │Completed │
         └──────────┘
```
---

# 💳 Transaction Flow

The internal wallet system follows an atomic transaction model.

```text
                    Project Completion
                           │
                           ▼
                  ┌─────────────────┐
                  │ Validate Project│
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Begin Transaction│
                  └────────┬────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
          Debit Requester      Credit Assignee
                 │                   │
                 └─────────┬─────────┘
                           ▼
                  Transaction Commit
                           │
                           ▼
                    Notifications
```

> ⚠️ `.env`, virtual environments, database files, `node_modules/`, build output, and generated secrets should not be committed to GitHub.

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd workfolio
```

---

# 🐍 Backend Setup

## 2. Create Virtual Environment

### Windows PowerShell

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

# 📧 Gmail SMTP Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Configure Gmail SMTP when email delivery is required.

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-gmail@gmail.com
SMTP_APP_PASSWORD=your-app-password
```

### ⚠️ Important

* Use a Gmail account intended for application email delivery.
* Enable Google 2-Step Verification.
* Use a Gmail App Password.
* Do not use your normal Gmail password.
* Never commit `.env` to GitHub.
* Never place SMTP credentials directly inside source code.

If SMTP is not configured, development OTP behavior can be used for local testing.

---

# ▶️ Running the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

The application starts with empty business tables.

User-created data such as profiles, posts, opportunities, applications, messages, notifications, wallets, and reviews is generated through real application actions.

---

# ⚛️ Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

---

# 📊 Project Status

🚧 **Academic / Full-Stack Project**

Workfolio is a full-stack professional networking and work marketplace project focused on demonstrating:

* 👤 Unified user identity
* 💼 Professional opportunities
* 🤝 Work marketplace workflows
* 📰 Social networking
* 📋 Project lifecycle management
* 💬 Communication
* 💰 Internal wallet transactions
* ⭐ Professional reputation
* 🤖 AI-assisted database interactions
* 🔐 Authentication and application security

---

# 🧭 Design Principles

Workfolio follows these core principles:

```text
                    ┌─────────────────────┐
                    │   ONE ACCOUNT       │
                    │   ONE PROFILE       │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
        Professional       Work Marketplace    Social Feed
           Identity             │                 │
             │                  ▼                 │
             │              Projects              │
             │                  │                 │
             └──────────────────┼─────────────────┘
                                ▼
                         Unified Experience
```

### 👤 Unified Identity

One account supports multiple professional contexts.

### 💼 Work + Networking

Professional networking and work opportunities exist within the same platform.

### 🔄 Explicit Workflows

Applications, acceptance, deadlines, revisions, resubmissions, and completion are represented as explicit state transitions.

### 🔐 Secure Authentication

Registration, OTP verification, password hashing, and sessions are handled through backend-controlled authentication logic.

### 💰 Demo-Only Transactions

The wallet is designed for application demonstration and does not process real money.

### 🤖 Controlled AI

The AI assistant can route database-backed requests but does not automatically perform irreversible actions.

### 🗄️ Persistent Data

Business data is stored in a persistent SQLite database and created through real user actions.

---

# 📜 License

This project is developed for **educational and academic purposes**.

---

# 📫 Contact

**Gunda Tejeswara Rao**

GitHub:

[https://github.com/gundatejeswararao7](https://github.com/gundatejeswararao7)

---

# ⭐ Support

If you find **Workfolio** useful or interesting, consider giving the repository a ⭐ on GitHub.

<div align="center">

### 💼 Built with React + TypeScript + FastAPI + SQLite

**Workfolio — One Account. One Profile. Multiple Ways to Work. 🚀**

</div>
