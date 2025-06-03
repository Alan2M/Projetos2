const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl : 'https://solidreamss-ergee5addqeyewg9.brazilsouth-01.azurewebsites.net/' ,
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
