import React, { useEffect, useState } from "react";
import axios from "axios";

const Participants = () => {
  // useStates
  const [participants, setParticipants] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const [editIndex, setEditIndex] = useState(null);


  const [editingElement, setEditingElement] = useState({
    id: '',
    name: '',
    email: '',
  });


  // Fetch participants data
  const fetchParticipants = async () => {
    try {
      const response = await axios.get(`/api/participants`);
      setParticipants(response.data);
    } catch (error) {
      console.error('Error fetching data: ', error);
    }
  };


  useEffect(() => {
    fetchParticipants();
  }, []);


  // Validation for input
  const validateInputs = () => {
    // Participant name cannot be more than 600 char
    if (editingElement.participantName.length > 600) {
      alert('Name should not exceed 600 characters.');
      return false;
    }
    return true;
  };


  // Handle create or update participant
  const handleCreateOrUpdate = async () => {
    if (isEditing) {
      await axios.put(`/api/participants/${editingElement.id}`, editingElement);
    } else {
      await axios.post(`/api/participants`, { ...editingElement, id: editingElement.id !== '' ? editingElement.id : undefined });
    }
    fetchParticipants();
    resetForm();
  };


  // Edit mode
  const handleEdit = (index, item) => {
    setIsEditing(true);
    setEditIndex(index);
    setEditingElement(item);
  };


  // Deletes id
  const handleDelete = async (id) => {
    await axios.delete(`/api/participants/${id}`);
    fetchParticipants();
  };


  // Handles the change
  const handleInputChange = (e) => {
    setEditingElement({ ...editingElement, [e.target.name]: e.target.value });
  };


  // Resets the form
  const resetForm = () => {
    setEditingElement({
      id: '',
      name: '',
      email: '',
    });
    setIsEditing(false);
    setEditIndex(null);
  };


  return (
    <div>
      <div className="form">
        <input name="id" value={editingElement.id} onChange={handleInputChange}
          placeholder="Participant UUID" />
        <input name="name" value={editingElement.name} onChange={handleInputChange}
          placeholder="Name (max 600 characters)" />
        <input name="email" value={editingElement.email} onChange={handleInputChange}
          placeholder="Email" />
      </div>


      <button onClick={handleCreateOrUpdate}>
        {isEditing ? 'Save Changes' : 'Create'}
      </button>


      {participants.map((participant, index) => (
        <div key={index} style={{
          marginBottom: '20px',
          padding: '10px',
          border: '1px solid #ccc',
          borderRadius: '8px',
          backgroundColor: '#f9f9f9'
        }}>
          <p><strong>UUID:</strong> {participant.id}</p>
          <p><strong>Name:</strong> {participant.name}</p>
          <p><strong>Email:</strong> {participant.email}</p>

          <div style={{ marginTop: '10px' }}>
            <button onClick={() => handleEdit(index, participant)} style={{ marginRight: '10px' }}>Edit</button>
            <button onClick={() => handleDelete(participant.id)}>Delete</button>
          </div>
          <hr />
        </div>
      ))}

    </div>
  );
};


export default Participants;
