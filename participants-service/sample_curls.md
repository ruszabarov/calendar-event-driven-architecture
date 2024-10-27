### Creating a Participant
```bash
curl -X POST http://localhost:8080/participants \
     -H "Content-Type: application/json" \
     -d '{"name": "Jane Doe", "email": "jane@example.com"}'
```

### Creating a Participant with ID
```bash
curl -X POST http://localhost:8080/participants \
     -H "Content-Type: application/json" \
     -d '{"id": "<participant_id>", "name": "Jane Doe", "email": "jane@example.com"}'

```

### Getting all participants
```bash
curl -X GET http://localhost:8080/participants
```

### Getting a Participant by ID
```bash
curl -X GET http://localhost:8080/participants/<participant_id>
```

### Getting multiple Participants by IDs
```bash
curl -X GET "http://localhost:8080/participants?ids=<id1>,<id2>"
```


### Updating a Participant
```bash
curl -X PUT http://localhost:8080/participants/<participant_id> \
     -H "Content-Type: application/json" \
     -d '{"name": "Jane Smith", "email": "jane.smith@example.com"}'
```

### Deleting a Participant
```bash
curl -X DELETE http://localhost:8080/participants/<participant_id>
```