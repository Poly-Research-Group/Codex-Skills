# Merge Audit Checklist

For every merge/join:

- [ ] Expected cardinality is documented before running the join.
- [ ] Left-table keys are checked for duplicates.
- [ ] Right-table keys are checked for duplicates.
- [ ] Join keys are standardized to compatible formats.
- [ ] Match rate is calculated.
- [ ] Unmatched left rows are saved or counted.
- [ ] Unmatched right rows are saved or counted when relevant.
- [ ] Row count before and after join is recorded.
- [ ] Row multiplication is checked.
- [ ] Keep/drop decisions are substantively justified.
