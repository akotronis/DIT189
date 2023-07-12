import React from 'react';
import AsyncSelect from 'react-select/async';

const marriageMenuStyles = {
  // Style for the selected value
  menuList: (provided) => ({
    ...provided,
    fontStyle: 'strong', // Make the font italic
    fontSize: '14px', // Adjust the font size as desired
    whiteSpace: 'pre-wrap',
    // fontFamily: 'Arial, sans-serif', // Change the font family
    // Add any other desired styles
  }),
};

export default function Search(props) {
  const loadOptions = (inputValue, callback) => {
    // Perform your async fetch request or API call here
    // Example:

    if (props.url.includes('marriage')) {
      inputValue = ''
    }


    fetch(props.url + inputValue)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);

        const options = data.map((item) => {
          let label = null
          if (props.url.includes('marriage')) {
            label = `Marriage ID:  ${item.id}\nStarting date: ${item.start_date}\nSpouses:\n   1.  Fullname (VAT):  ${item.users[0].last_name} ${item.users[0].first_name} (${item.users[0].vat_num})\n        Email:                  ${item.users[0].email}\n   2.  Fullname (VAT):  ${item.users[1].last_name} ${item.users[1].first_name} (${item.users[1].vat_num})\n        Email:                  ${item.users[1].email}`;
          } else if (
            props.url.includes('LAWYER') ||
            props.url.includes('NOTARY')
          ) {
            label = `Fullname (VAT):  ${item.last_name} ${item.first_name} (${item.vat_num})\nEmail:  ${item.email}`;
          }
          return {
            value: item.id,
            label: label,
            data: "kati",
          };
        });
        callback(options);
      })
      .catch((error) => {
        console.error(error);
        callback([]);
      });
  };

  return (
    <AsyncSelect
      isClearable
      value={props.value}
      onChange={props.onChange}
      // cacheOptions
      styles={marriageMenuStyles} // Add the custom styles
      loadOptions={loadOptions}
      // placeholder="Select a notary..."
    />
  );
}
