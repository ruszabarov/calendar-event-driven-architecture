import React, { useEffect, useState } from "react";
import axios from "axios";

const Calendars = () => {
  // useStates
  const [calendars, setCalendars] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const [editIndex, setEditIndex] = useState(null);
  const [newMeetingUUID, setNewMeetingUUID] = useState('');


  const [editingElement, setEditingElement] = useState({
    id: '',
    title: '',
    details: '',
    meetings: ''
  });

  // Fetch calendar data
  const fetchCalendars = async () => {
    try {
      const response = await axios.get(`/api/calendars`);
      setCalendars(response.data);
    } catch (error) {
      console.error("Error fetching calendars data: ", error);
    }
  };

  // Use effect fetches calendar data from the server
  useEffect(() => {
    fetchCalendars();
  }, []);

  // Validations
  const validateInputs = () => {
    // Title is not longer than 2000 chars
    if (editingElement.title.length > 2000) {
      alert("Title should not exceed 2000 characters.");
      return false;
    }
    // Details is not longer than 10000 chars
    if (editingElement.details.length > 10000) {
      alert("Details should not exceed 10000 characters.");
      return false;
    }
    return true;
  };

  // Handle creation or update of a calendar
  const handleCreateOrUpdate = async () => {
    if (!validateInputs()) return;

    if (isEditing) {
      await axios.put(`/api/calendars/${editingElement.id}`, editingElement);
    } else {
      await axios.post(`/api/calendars`, {
        ...editingElement,
        id: editingElement.id ? editingElement : undefined,
        meetings: [editingElement.meetings]
      });
    }
    fetchCalendars();
    resetForm();
  };

  // Edit mode
  const handleEdit = (index, item) => {
    setIsEditing(true);
    setEditIndex(index);
    setEditingElement({ ...item, meetings: "" });
  };

  // Handles delete
  const handleDelete = async (id) => {
    await axios.delete(`/api/calendars/${id}`);
    fetchCalendars();
  };

  // Handles the change
  const handleInputChange = (e) => {
    setEditingElement({ ...editingElement, [e.target.name]: e.target.value });
  };

  // Resets form
  const resetForm = () => {
    setEditingElement({
      id: '',
      title: '',
      details: '',
      meetings: ''
    });
    setIsEditing(false);
    setEditIndex(null);
  };

  const handleMeetingUUIDChange = (e) => {
    setNewMeetingUUID(e.target.value);
  };

  const handleAddMeeting = async () => {
    if (newMeetingUUID) {
      try {
        const response = await axios.get(`/api/calendars/${editingElement.id}/addMeeting/${newMeetingUUID}`);
        setCalendars(calendars.map(calendar => calendar.id === response.data.id ? response.data : calendar));
        setNewMeetingUUID('');
      } catch (error) {
        console.error('Error adding participant: ', error);
      }
    }
  };

  return (
    <div>
      <div className="form">
        <input name="uuid" value={editingElement.id} onChange={handleInputChange} placeholder="Calendar UUID" />
        <input name="title" value={editingElement.title} onChange={handleInputChange}
          placeholder="Title (max 2000 characters)" />
        <textarea name="details" value={editingElement.details} onChange={handleInputChange}
          placeholder="Details (max 10000 characters)" />
        <input name="meetings" value={editingElement.meetings} onChange={handleInputChange}
          placeholder="Meeting ID" />
      </div>

      <button onClick={handleCreateOrUpdate}>
        {isEditing ? 'Save Changes' : 'Create'}
      </button>

      <div className="meeting-form" style={{ marginBottom: '50px' }}>
        <h4>Add Meeting by UUID</h4>
        <input name="meetingUUID" value={newMeetingUUID} onChange={handleMeetingUUIDChange}
          placeholder="Meeting UUID" />
        <button onClick={handleAddMeeting}>Add Meeting</button>
      </div>

      {calendars.map((calendar, index) => (
        <div key={index} style={{
          marginBottom: '30px',
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '8px',
          backgroundColor: '#f9f9f9'
        }}>
          <p><strong>UUID:</strong> {calendar.id}</p>
          <p><strong>Title:</strong> {calendar.title}</p>
          <p><strong>Details:</strong> {calendar.details}</p>

          {calendar.meetings && calendar.meetings.length > 0 && (
            <>
              <h4>Meetings:</h4>
              {calendar.meetings.map((meeting, index) => (
                <div key={index} style={{ marginLeft: '20px', marginBottom: '10px' }}>
                  <p><strong>UUID:</strong> {meeting.id}</p>
                  <p><strong>Title:</strong> {meeting.title}</p>
                  <p><strong>Date & Time:</strong> {meeting.datetime}</p>
                  <p><strong>Location:</strong> {meeting.location}</p>
                  <p><strong>Details:</strong> {meeting.details}</p>
                  <hr />
                </div>
              ))}
            </>
          )}

          <div style={{ marginTop: '10px' }}>
            <button onClick={() => handleEdit(index, calendar)} style={{ marginRight: '10px' }}>Edit</button>
            <button onClick={() => handleDelete(calendar.id)}>Delete</button>
          </div>
          <hr />
        </div>
      ))}

    </div>
  );
};

export default Calendars;
