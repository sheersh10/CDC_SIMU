# Placement Simulation Model - Conceptual Flowchart

## Process Flow Diagram

```mermaid
flowchart TD
    Start([Day Begins]) --> CompanyArrives[Company Arrives<br/>Releases Eligibility Criteria]
    
    CompanyArrives --> CheckEligible{Students Check<br/>Eligibility}
    
    CheckEligible -->|Eligible| Apply[Students Apply<br/>for Test]
    CheckEligible -->|Not Eligible| Wait1[Wait for Next<br/>Company]
    
    Apply --> ProfileScore[Profile Score<br/>Calculation]
    
    ProfileScore --> ShortlistTest{Company Selects<br/>for Interview<br/>Based on Profile}
    
    ShortlistTest -->|Selected| Interview[Interview Round]
    ShortlistTest -->|Rejected| Wait2[Wait for Next<br/>Company]
    
    Interview --> InterviewScore[Interview Score<br/>Calculation]
    
    InterviewScore --> FinalSelection{Company Makes<br/>Final Selection}
    
    FinalSelection -->|Offer Received| Placed[Student Placed ✓]
    FinalSelection -->|Rejected| Unplaced[Student Remains<br/>Unplaced]
    
    Placed --> Exit1([End of Day])
    
    Wait1 --> NextCompany{More Companies<br/>Today?}
    Wait2 --> NextCompany
    Unplaced --> NextCompany
    
    NextCompany -->|Yes| CompanyArrives
    NextCompany -->|No| DayEnd{End of Day<br/>Check}
    
    DayEnd --> PlacementCheck{Student<br/>Placed?}
    
    PlacementCheck -->|Yes| Exit2([Success - Placed])
    PlacementCheck -->|No| Decision{Opt to Continue?<br/>Probability-based}
    
    Decision -->|Continue| NextDay([Next Day<br/>Starts])
    Decision -->|Opt Out| Exit3([Opts Out - Unplaced])
    
    NextDay --> Start
    
    style Start fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    style CompanyArrives fill:#4a90e2,stroke:#333,stroke-width:2px,color:#fff
    style Placed fill:#2ecc71,stroke:#333,stroke-width:3px,color:#fff
    style Exit2 fill:#27ae60,stroke:#333,stroke-width:3px,color:#fff
    style Exit3 fill:#e74c3c,stroke:#333,stroke-width:2px,color:#fff
    style Decision fill:#f39c12,stroke:#333,stroke-width:2px,color:#fff
    style Interview fill:#9b59b6,stroke:#333,stroke-width:2px,color:#fff
```

## Compact Version (For Presentations)

```mermaid
flowchart LR
    A([Company Arrives]) --> B{Eligibility<br/>Check}
    B -->|Eligible| C[Apply & Test]
    B -->|Not Eligible| H[Wait]
    C --> D[Profile Score]
    D --> E{Shortlist for<br/>Interview?}
    E -->|Yes| F[Interview]
    E -->|No| H
    F --> G{Final<br/>Selection?}
    G -->|Placed| I[✓ Placed]
    G -->|Rejected| H
    H --> J{More<br/>Companies?}
    J -->|Yes| A
    J -->|No| K{Continue to<br/>Next Day?}
    K -->|Yes| L([Next Day])
    K -->|No| M[Opt Out]
    L --> A
    
    style A fill:#4a90e2,color:#fff
    style I fill:#2ecc71,color:#fff,stroke-width:3px
    style M fill:#e74c3c,color:#fff
    style K fill:#f39c12,color:#000
```

## Ultra-Compact Version (Minimal)

```mermaid
flowchart TD
    A[Company: Eligibility] --> B[Eligible Students Apply]
    B --> C[Profile Score → Shortlist]
    C --> D[Interview Score → Selection]
    D --> E{Placed?}
    E -->|Yes| F[✓ End]
    E -->|No| G{Day End?}
    G -->|No| A
    G -->|Yes| H{Opt Out?}
    H -->|No| I[Next Day]
    H -->|Yes| J[Exit Unplaced]
    I --> A
    
    style F fill:#2ecc71,color:#fff,stroke-width:3px
    style J fill:#e74c3c,color:#fff
```

## Key Process Elements

### 1. **Company Arrival Phase**
- Company releases eligibility criteria (CGPA, Department, Skills)
- Students check if they meet requirements

### 2. **Application & Profile Scoring**
- Eligible students apply
- Profile score calculated based on:
  - CGPA
  - Skills match
  - Domain alignment

### 3. **Interview Shortlisting**
- Company selects top candidates based on profile score
- Shortlisted students proceed to interview

### 4. **Interview & Final Selection**
- Interview score calculated
- Final selection based on interview performance
- Selected students receive offers

### 5. **Daily Cycle Management**
- Unplaced students wait for next company (same day)
- At day end, probability-based decision to continue or opt out
- Students opting to continue move to next day

## Model Features

✅ **Multi-stage selection** (Eligibility → Profile → Interview)  
✅ **Dynamic scoring** (Profile score + Interview score)  
✅ **Daily cycles** (Multiple companies per day)  
✅ **Student agency** (Probability-based opt-out decisions)  
✅ **Realistic constraints** (Eligibility filtering, limited seats)

---

*Use the version that best fits your presentation space and detail requirements*
