# CareFlow: ER Process Design

## Goal
Simulate hospital Emergency Room event logs with built-in inefficiencies,
so process mining can discover them later.

## Event log format
| Column | Type | Meaning |
|---|---|---|
| Case_ID | Case attribute | One patient visit |
| Activity | Event | The step that happened |
| Timestamp | Event | When it happened |
| Condition | Case attribute | The patient's medical problem |
| Age_Group | Case attribute | Child, Adult or Senior |
| Ward | Event attribute | Filled only on the Ward Admission step |

Case attributes stay the same for the whole visit. Event attributes belong
to one step.

## Patient conditions
| Condition | Share of patients | X-Ray | Lab Test | Admission | Ward |
|---|---|---|---|---|---|
| Fracture or injury | 15% | 85% | 10% | 25% | Orthopedic |
| Chest pain | 10% | 30% | 80% | 40% | Cardiology |
| Fever or infection | 25% | 10% | 70% | 15% | General |
| Stomach pain | 15% | 20% | 60% | 20% | General |
| Minor illness | 35% | 5% | 15% | 2% | General |

## Age groups
| Age group | Share of patients |
|---|---|
| Child | 20% |
| Adult | 55% |
| Senior | 25% |

## Activities
Registration, Triage, Doctor Consultation, X-Ray, Lab Test, Doctor Review,
Ward Admission, Pharmacy, Billing, Discharge.

## Patient flow
1. Registration, then Triage, then Doctor Consultation (every patient).
   If no tests are needed, the doctor gives the conclusion at this step.
2. Tests: the doctor may order an X-Ray and/or a Lab Test, based on the
   chances for the patient's condition.
3. Doctor Review (every patient who had any test): the doctor reads the
   results and gives the final conclusion.
4. Admission decision, based on the condition's chance of admission.
   - Admitted: Ward Admission (ward depends on condition), then Discharge.
   - Not admitted: Pharmacy (60% of patients), then Billing, then Discharge.

## Planned inefficiencies (to be discovered later)
- About 40% of patients sent for an X-Ray return to Triage afterwards
  (loop-back caused by missing paperwork), then continue to Doctor Review.
- Long waits at Doctor Consultation during busy hours.
- Slow Pharmacy in the evening.

## Assumed step durations (minutes)
| Activity | Duration |
|---|---|
| Registration | 2 to 8 |
| Triage | 5 to 15 |
| Doctor Consultation | 10 to 30 |
| X-Ray | 10 to 30 |
| Lab Test | 20 to 60 |
| Doctor Review | 5 to 15 |
| Ward Admission | 120 to 480 |
| Pharmacy | 5 to 25 |
| Billing | 3 to 12 |
| Discharge | 3 to 10 |

## Ideal pathway (for conformance checking in Week 4)
Registration, Triage, Doctor Consultation, (tests), Doctor Review (if tests),
then Pharmacy and Billing or Ward Admission, then Discharge, with no return
to an earlier step.

## Generator progress
- v1: normal path only (Registration, Triage, Doctor Consultation, Discharge).
- v2: adds Condition and Age_Group to every patient.
- v3: adds X-Ray and Lab Test (chances depend on condition), Doctor Review,
  and the 40% X-Ray to Triage loop-back.
- v4: adds admission, the Ward column, Pharmacy and Billing.
- Next: busy-hour delays and slow evening pharmacy, then scale to 10,000 patients.