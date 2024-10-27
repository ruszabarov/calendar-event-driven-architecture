import React, {useState, useEffect} from 'react';
import axios from 'axios';
import './Home.css';
import Attachments from "./Attachments";
import Meetings from "./Meetings";
import Calendars from "./Calendars";
import Participants from "./Participants";

const Home = () => {
    const [currentTab, setCurrentTab] = useState('Meetings');


    return (
        <div className="container">

            {/* TABS */}
            <div className="tabs">
                <button onClick={() => setCurrentTab('Meetings')}>Meetings</button>
                <button onClick={() => setCurrentTab('Calendars')}>Calendars</button>
                <button onClick={() => setCurrentTab('Participants')}>Participants</button>
                <button onClick={() => setCurrentTab('Attachments')}>Attachments</button>
            </div>

            <div>
                <div className="list">

                    {/* Meetings */}
                    {currentTab === 'Meetings' && <Meetings/>}

                    {/* Calendars */}
                    {currentTab === 'Calendars' && <Calendars/>}

                    {/* Participants */}
                    {currentTab === 'Participants' && <Participants/>}

                    {/* Attachments */}
                    {currentTab === 'Attachments' && <Attachments/>}
                </div>
            </div>
        </div>
    );
};

export default Home;
