---
title: "[TOPIC] example reference"
description: ""
---

# [TOPIC] examples

This reference contains a variety of examples using Dagster [TOPIC]. Each example contains:

- A summary
- Additional notes
- Links to relevant documentation
- A list of the APIs used in the example

---

## [Title of example]

[This example demonstrates [description of what the example accomplishes]

<!-- Example: This example demonstrates how to use resources in schedules. To specify a resource dependency, annotate the resource as a parameter to the schedule's function. -->

```python title="my_schedule.py"
@schedule(job=my_job, cron_schedule="* * * * *")
def logs_then_skips(context):
    context.log.info("Logging from a schedule!")
    return SkipReason("Nothing to do")
```

<!-- We need to fix the base table implemenatation before launch. This is a must. -->

| | |
|-|-|
| Notes | |
| Related docs | |
| APIs in this example | |

---

<!-- This section lists a few additional sources of inspiration, such as DOP and GitHub discussions. You shouldn't need to change anything here. -->

import InspirationList from '../partials/_InspirationList.md';

<InspirationList />