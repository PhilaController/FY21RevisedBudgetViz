import "core-js/stable";
import Vue from "vue";
import App from "@/App";
import router from "@/router";

Vue.config.productionTip = false;

// load and set the HTML template we are using
let audit_content = $(".audit-content");
audit_content.html(`<div id="app"></div>`);

function add_data_buttons() {

  // revenue button
  let revenue_url = "https://raw.githubusercontent.com/PhiladelphiaController/RevisedBudgetFY20-FY25/master/src/data/revenue_revisions.csv";
  let revenue_btn = `<a href="${revenue_url}" class="btn btn-primary btn-block btn-block">
            <i class="fas fa-download"></i>
            Download Revenue Data
        </a>`;

  // spending button
  let spending_url = "https://raw.githubusercontent.com/PhiladelphiaController/RevisedBudgetFY20-FY25/master/src/data/budget_revisions_by_major_class.csv";
  let spending_btn = `<a href="${spending_url}" class="btn btn-primary btn-block btn-block">
            <i class="fas fa-download"></i>
            Download Spending Data
        </a>`;

  // add download data button and remove the report button
  $(".entry-header .btn").after(revenue_btn).after(spending_btn).first().remove();
}

add_data_buttons()

// add help message
let helpMessage = `<p class='help-message mt-2'>
  Comments or feedback? Please contact
  <a href="mailto:controller.policy@phila.gov">controller.policy@phila.gov</a>.
  </p>`;
$(".back-link").after(helpMessage);


// mount the app
new Vue({
  router,
  render: h => h(App)
}).$mount("#app");