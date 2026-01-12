# Capital-Trace
Personal Budgeting tool- maybe something in the future

## Usage

### Requirements
- Python 3.11+
- Bank of America transaction exports (TXT format)

### Project Structure
Capital-Trace/     
├── budget/ # Core logic                
├── data/ # Bank statements (checking.txt, savings.txt)              
├── docs/ # Design notes              
└── README.md

### Running the Analysis
From the project root:

##### python -m budget.main

This will:

load checking and savings statements

compute current cash state

allocate envelopes by priority

calculate burn rates and runway

generate optimized envelope goals

print projections and risks

### Scenario Analysis (What-If Experiments)
Reduce discretionary spending by X%

To simulate the impact of cutting discretionary spending:
###### python -m budget.main --cut-discretionary 25
Example scenarios:
###### python -m budget.main --cut-discretionary 10
###### python -m budget.main --cut-discretionary 25
###### python -m budget.main --cut-discretionary 50

This mode:

does NOT modify envelopes

does NOT save state

only adjusts assumptions

recalculates projections and goals

Use this to understand how behavior changes affect survivability.

Important Design Notes

Envelopes represent current intent, not historical spending

Past transactions are used only for burn-rate analysis

All projections are pessimistic by design (worst-case buckets)

No money is ever created or destroyed (hard invariant)

If the invariant fails, the program will exit with an error.

## Development outline

### 1. Scope & Purpose

This system exists to:

Show true cash position

Enforce intentional spending via envelopes

Surface future risk early

Remove ambiguity about where money went

It is not optimized for:

Net worth tracking

Tax reporting

Perfect categorization

Real-time syncing

Accuracy > convenience. Awareness > automation.

### 2. Account Model (Hard Rules)
Cash Pool

Checking + Savings are merged into a single Cash Pool

Individual account balances are ignored for budgeting logic

The Cash Pool is the only source of envelope funding

Credit Card

Credit cards are liabilities

Credit cards are not cash

Credit card balance is tracked separately from the Cash Pool

### 3. Transaction Types (Exactly Three)

Every transaction MUST be classified as one and only one of the following:

#### 3.1. Income

Definition:
Money entering the Cash Pool from outside the system.

Examples:

Paychecks

Refunds

Interest

Cash deposits

Rules:

Income increases Cash Pool balance

Income is assigned to Unallocated

Income does NOT auto-fill envelopes

#### 3.2. Spending

Definition:
Money leaving the system in exchange for goods or services.

Examples:

Groceries

Rent

Dining

Subscriptions

Credit card purchases (at time of swipe)

Rules:

Spending reduces Cash Pool OR increases credit liability

Spending MUST be assigned to exactly one envelope

Spending reduces envelope balance immediately

#### 3.3. Transfer

Definition:
Money moving internally with no economic impact.

Examples:

Checking ↔ Savings

Credit card payments

Moving money between internal accounts

Rules:

Transfers do NOT affect envelopes

Transfers do NOT count as income or spending

Transfers exist only for reconciliation and balance tracking

### 4. Envelope System Rules
Envelope Definition

An envelope represents reserved cash with intent.

Core Envelopes

Unallocated (mandatory, cannot be deleted)

User-defined spending envelopes

Allocation Rules

All income enters Unallocated

Money must be explicitly moved from Unallocated → envelopes

Allocation is a conscious action, not automatic

Spending Rules

Every spending transaction must reference exactly one envelope

If an envelope goes negative, it is overspent

Overspending must be corrected by reallocating from another envelope

Invariant (This Must Always Hold)
Sum of all envelope balances == Cash Pool balance


If this is false, the system is broken.

### 5. Credit Card Rules (No Exceptions)
Credit Card Purchases

Treated as spending immediately

Assigned to an envelope at time of transaction

Reduce envelope balance immediately

Increase credit card liability

Credit Card Payments

Classified as transfers

Reduce Cash Pool balance

Reduce credit card liability

Do NOT touch envelopes

Rule of Truth:
You pay for things when you buy them, not when you pay the card.

### 6. Time & Reporting Rules
Dates

Use posted date, not authorization date

Transactions belong to the period they post

Reporting Periods

Day / week / month are simple rollups

No retroactive reclassification after reconciliation

### 7.  Projection Rules (Future Balance)
Projection Definition

A projection is a deterministic simulation, not a guess.

Inputs:

Current Cash Pool balance

Envelope balances

Scheduled income

Scheduled fixed spending

Known credit card obligations

Projection Must:

Never assume “future discipline”

Never auto-ignore overspending

Surface lowest balance point

If a projection is wrong, the inputs are wrong — not the math.

### 8.  Workflow Assumptions (Be Honest)

CSV imports happen weekly

Manual review is expected

Perfection is not required, consistency is

If this workflow is skipped, numbers are untrusted.

### 9.  Non-Goals (Explicitly Out of Scope)

Investment performance tracking

Tax categorization

Real-time syncing

Budget gamification