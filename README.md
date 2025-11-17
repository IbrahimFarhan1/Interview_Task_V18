# Project Cost Estimation – Odoo Custom Module V 18

## 🚀 Live Demo
The module is deployed and available for review at:

🔗 **http://38.242.156.95:8069/odoo/project**

---

The module adds cost estimation functionality to Odoo Projects, including cost breakdowns, workflow approval, permissions, sequences, and email notifications.

---

## 📌 Features Overview

### ✅ Project Cost Estimates
- New model: `project.cost.estimate`
- Linked to Odoo Projects
- Computed total cost based on breakdown lines

### ✅ Cost Breakdown Lines
- New model: `project.cost.breakdown`
- Fields: description, unit cost, quantity, subtotal
- Subtotal computed per line
- One-to-many relationship with cost estimates

### ✅ Workflow Logic
Each estimate moves through a defined approval workflow:

| State       | Action            | Who Can Do It |
|-------------|-------------------|----------------|
| `draft`     | Submit            | Project Users |
| `submitted` | Approve/Reject    | Approvers     |
| `approved`  | —                 | Read-only     |
| `rejected`  | —                 | Read-only     |

- Fields become **read-only** after submission.
- Approval and rejection trigger **email notifications**.

### ✅ Security & Access Rules

The module defines three security groups:

#### 🔹 **Project User**
- Can create estimates
- Can edit only their own estimates
- Can submit estimates

#### 🔹 **Project Admin**
- Can view all estimates for projects they manage
- Can submit estimates

#### 🔹 **Approval Group**
- Can see all submitted estimates
- Can approve or reject
- Cannot edit estimates

Record rules ensure proper visibility and permissions for each group.

---

## 📬 Email Notifications

When an estimate is **approved** or **rejected**, the system sends an automatic email to the estimate creator.

Email template supports:
- Dynamic values (estimate name, project name, amount)
- QWeb fields for safe rendering
- Configurable email_from / email_to

---

## 🖥️ User Interface Enhancements

### ✔ Smart Button on Project Form
A smart button shows the number of cost estimates linked to the project and opens them in a view.

### ✔ Cost Estimate Kanban View
A custom kanban view provides:
- Status
- Project
- Total estimated cost

### ✔ Latest Estimate on Project Kanban
Each project kanban card displays its **latest** cost estimate automatically.

