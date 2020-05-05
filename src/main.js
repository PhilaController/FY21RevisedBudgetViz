import Vue from "vue";
import App from "@/App";
import router from "@/router";

// make FA does not watch SVG elements
if (window.FontAwesome) window.FontAwesome.config.observeMutations = false;
Vue.config.productionTip = false;

// load and set the HTML template we are using
let audit_content = $(".audit-content");
audit_content.html(`<div id="app"></div>`);

function add_data_buttons() {

  // add a new button
  let url = `https://spreadsheets.google.com/tq?tqx=out:csv&key=${GID}&sheet=${SHEETNAME}`;
  let btn = `<a href="${url}" class="btn btn-primary btn-block btn-block">
            <i class="fas fa-download"></i>
            Download Data
        </a>`;

  // add download data button and remove the report button
  $(".entry-header .btn").after(btn);
  $(".entry-header .btn")
    .first()
    .remove();
}


// add help message
let helpMessage = `<p class='help-message'>
  Comments or feedback? Please contact
  <a href="mailto:controller.policy@phila.gov">controller.policy@phila.gov</a>.
  </p>`;
$(".back-link").after(helpMessage);


// mount the app
new Vue({
  router,
  render: h => h(App)
}).$mount("#app");