import React, { useEffect, useState } from "react";
import axios from "axios";

const Meetings = () => {
  const [meetings, setMeetings] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const [editIndex, setEditIndex] = useState(null);
  const [newParticipantUUID, setNewParticipantUUID] = useState('');
  const [newAttachmentUUID, setNewAttachmentUUID] = useState('');

  const [editingElement, setEditingElement] = useState({
    id: '',
    title: '',
    details: '',
    datetime: '',
    location: '',
    participantIds: '',
  });

  const fetchMeetings = async () => {
    try {
      const response = await axios.get(`/api/meetings`);
      setMeetings(response.data);
    } catch (error) {
      console.error('Error fetching data: ', error);
    }
  };

  useEffect(() => {
    fetchMeetings();
  }, []);

  const handleCreate = async () => {
    await axios.post(`/api/meetings`, {
      ...editingElement,
      id: editingElement.id ? editingElement.id : undefined,
      participants: [editingElement.participantIds],
      attachments: [],
      calendars: [],
      participantIds: undefined,
    });
    fetchMeetings();
    resetForm();
  }

  const handleEdit = (index, item) => {
    setIsEditing(true);
    setEditIndex(index);
    setEditingElement(item);
  };

  const handleDelete = async (index, id) => {
    await axios.delete(`/api/meetings/${id}`);
    fetchMeetings();
  };

  const handleInputChange = (e) => {
    setEditingElement({ ...editingElement, [e.target.name]: e.target.value });
  };

  const handleParticipantUUIDChange = (e) => {
    setNewParticipantUUID(e.target.value);
  };

  const handleAddParticipant = async () => {
    if (newParticipantUUID) {
      try {
        await axios.get(`/api/meetings/${editingElement.id}/addParticipant/${newParticipantUUID}`);
        fetchMeetings();
        setNewParticipantUUID('');
      } catch (error) {
        console.error('Error adding participant: ', error);
      }
    }
  };

  const handleAttachmentUUIDChange = (e) => {
    setNewAttachmentUUID(e.target.value);
  };

  const handleAddAttachment = async () => {
    if (newAttachmentUUID) {
      try {
        await axios.get(`/api/meetings/${editingElement.id}/addAttachment/${newAttachmentUUID}`);
        fetchMeetings();
        setNewAttachmentUUID('');
      } catch (error) {
        console.error('Error adding participant: ', error);
      }
    }
  };

  const handleUpdate = async () => {
    const updatedItem = {
      id: editingElement.id,
      title: editingElement.title,
      details: editingElement.details,
      datetime: editingElement.datetime,
      location: editingElement.location,
    };
    const response = await axios.put(`/api/meetings/${updatedItem.id}`, updatedItem);
    setMeetings(meetings.map(meeting => meeting.id === response.data.id ? response.data : meeting));
    resetForm();
  };

  const resetForm = () => {
    setEditingElement({
      id: '',
      title: '',
      details: '',
      datetime: '',
      location: '',
    });
    setIsEditing(false);
    setEditIndex(null);
  };

  return (
    <div>
      <div className="form">
        <input name="uuid" value={editingElement.id} onChange={handleInputChange}
          placeholder="Meeting UUID" />
        <input name="title" value={editingElement.title} onChange={handleInputChange}
          placeholder="Title" />
        <input name="datetime" value={editingElement.datetime} onChange={handleInputChange}
          placeholder="Date and Time (YYYY-MM-DD HH:MM AM/PM)" />
        <input name="location" value={editingElement.location} onChange={handleInputChange}
          placeholder="Location" />
        <textarea name="details" value={editingElement.details} onChange={handleInputChange}
          placeholder="Details" />
        <input name="participantIds" value={editingElement.participantIds} onChange={handleInputChange}
          placeholder="Participant ID" />
      </div>

      <button onClick={isEditing ? handleUpdate : handleCreate}>
        {isEditing ? 'Save Changes' : 'Create'}
      </button>

      <div className="participant-form">
        <h4>Add Participant by UUID</h4>
        <input name="participantUUID" value={newParticipantUUID} onChange={handleParticipantUUIDChange}
          placeholder="Participant UUID" />
        <button onClick={handleAddParticipant}>Add Participant</button>
      </div>

      <div className="attachment-form" style={{ marginBottom: '50px' }}>
        <h4>Add Attachment by UUID</h4>
        <input name="attachmentUUID" value={newAttachmentUUID} onChange={handleAttachmentUUIDChange}
          placeholder="Attachment UUID" />
        <button onClick={handleAddAttachment}>Add Attachment</button>
      </div>

      {meetings && meetings.map((meeting, index) => (
        <div style={{
          marginBottom: '30px',
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '8px',
          backgroundColor: '#f9f9f9'
        }} key={index}>
          <h3>{meeting.title}</h3>
          <p><strong>UUID:</strong> {meeting.id}</p>
          <p><strong>Date & Time:</strong> {meeting.datetime}</p>
          <p><strong>Location:</strong> {meeting.location}</p>
          <p><strong>Details:</strong> {meeting.details}</p>

          {meeting.calendars.length > 0 && (
            <>
              <h4>Calendars:</h4>
              {meeting.calendars.map((calendar, index) => (
                <div key={index} style={{ marginLeft: '20px' }}>
                  <p><strong>UUID:</strong> {calendar.id}</p>
                  <p><strong>Title:</strong> {calendar.title}</p>
                  <p><strong>Details:</strong> {calendar.details}</p>
                </div>
              ))}
            </>
          )}

          {meeting.participants.length > 0 && (
            <>
              <h4>Participants:</h4>
              {meeting.participants.map((participant, index) => (
                <div key={index} style={{ marginLeft: '20px' }}>
                  <p><strong>UUID:</strong> {participant.id}</p>
                  <p><strong>Name:</strong> {participant.name}</p>
                  <p><strong>Email:</strong> {participant.email}</p>
                </div>
              ))}
            </>
          )}

          {meeting.attachments.length > 0 && (
            <>
              <h4>Attachments:</h4>
              {meeting.attachments.map((attachment, index) => (
                <div key={index} style={{ marginLeft: '20px' }}>
                  <p><strong>UUID:</strong> {attachment.id}</p>
                  <p><strong>URL:</strong> {attachment.url}</p>
                </div>
              ))}
            </>
          )}

          <div style={{ marginTop: '10px' }}>
            <button onClick={() => handleEdit(index, meeting)} style={{ marginRight: '10px' }}>Edit</button>
            <button onClick={() => handleDelete(index, meeting.id)}>Delete</button>
          </div>
          <hr />
        </div>
      ))}

    </div>
  )
}

export default Meetings;
