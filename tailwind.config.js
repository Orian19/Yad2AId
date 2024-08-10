export const content = [
  './frontend/extension/*.{html,js}', // Adjust paths as needed
];

export const theme = {
  extend: {},
};

export const daisyui = {
  themes: ["light", "dark"], // Add more themes as needed
};

export const plugins = [require('daisyui')];
