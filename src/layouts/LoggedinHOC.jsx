import React, { useState } from 'react';
import { useAccessToken } from '../context/Auth';
import { decodeAccessToken } from '../utils/keycloak_utils';
import { useEffect } from 'react';
import { USERS_URL } from '../config/config';

export const LoggedInHOC = (props) => {
  let [user, setUser] = useState([]);

  const { token } = useAccessToken();

  const userEmail = decodeAccessToken(token.accessToken).email;

  // Fetch data when the component mounts
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(USERS_URL + userEmail, {
          headers: {
            Authorization: `Bearer ${token.accessToken}`,
          },
        }); // Replace with your actual API endpoint
        const userData = await response.json();
        setUser(userData[0]);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, [token.accessToken, userEmail, setUser]);

  const ClonedChildren = React.cloneElement(props.children, { user });

  return <div className="hoc">{ClonedChildren}</div>;
};
