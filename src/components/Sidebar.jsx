import { AtSignIcon, CalendarIcon, EditIcon } from '@chakra-ui/icons';
import { ListItem, List, ListIcon } from '@chakra-ui/react';
import React from 'react';
import { NavLink } from 'react-router-dom';

export default function Sidebar() {
  return (
    <List color="white" fontSize="1.2rem" spacing={4}>
      <ListItem>
        <NavLink to="/">
          <ListIcon as={CalendarIcon} color="white" />
          Main page
        </NavLink>
      </ListItem>
      {/* <ListItem>
        <NavLink to="/profile">
          <ListIcon as={EditIcon} color="white" />
          Profile
        </NavLink>
      </ListItem> */}
      {/* <ListItem>
        <NavLink to="/create">
          <ListIcon as={AtSignIcon} color="white" />
          My Cases
        </NavLink>
      </ListItem> */}
    </List>
  );
}
