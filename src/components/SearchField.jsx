import React from 'react';
const url = 'https://api.github.com/search/users?q=John&per_page=5';
import AsyncSelect from 'react-select/async';

const options = [
  { value: 'chocolate', label: 'Chocolate' },
  { value: 'strawberry', label: 'Strawberry' },
  { value: 'vanilla', label: 'Vanilla' },
];

export default function Search(props) {
  const loadOptions = (inputValue, callback) => {
    // Perform your async fetch request or API call here
    // Example:
    fetch(`https://api.github.com/search/users?q=${inputValue}&per_page=5`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        const options = data.items.map((item) => ({
          value: item.login,
          label: item.login,
        }));
        callback(options);
      })
      .catch((error) => {
        console.error(error);
        callback([]);
      });
  };

  return (
    <AsyncSelect isClearable
      value={props.value}
      onChange={props.onChange}
      cacheOptions
      loadOptions={loadOptions}
      placeholder="Select a notary..."
    />
  );
}
