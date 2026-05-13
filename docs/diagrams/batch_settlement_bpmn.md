# BPMN Diagram: Daily Restaurant Settlement Pipeline

```mermaid
flowchart LR
    Start((Start: Daily scheduled job)) --> ExtractOrders[Extract completed orders from PostgreSQL]

    ExtractOrders --> ValidateOrders{Are completed orders available?}

    ValidateOrders -- No --> NoData[Write no-data pipeline log]
    NoData --> EndNoData((End))

    ValidateOrders -- Yes --> GroupByRestaurant[Group orders by restaurant]

    GroupByRestaurant --> CalculateTotals[Calculate total revenue, commission, and payout]

    CalculateTotals --> GenerateSettlement[Generate settlement records]

    GenerateSettlement --> SaveSettlement[Save settlement results to database]

    SaveSettlement --> NotifyOwners[Prepare restaurant owner settlement summary]

    NotifyOwners --> WriteLog[Write pipeline execution log]

    WriteLog --> End((End: Settlement completed))
```

## Description

This BPMN-style diagram represents the daily restaurant settlement pipeline. The pipeline starts as a scheduled batch job. It extracts completed orders from PostgreSQL, validates whether there is data to process, groups orders by restaurant, calculates revenue and payout values, stores settlement results, and writes execution logs. If no completed orders are found, the pipeline records a no-data log and finishes without generating settlement records.