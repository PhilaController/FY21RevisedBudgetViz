<template>
  <div class="home-page text-left ml-3 mr-3">
    <p>
      On May 1, 2020, Mayor Kenney released a
      <a
        href="https://www.phila.gov/media/20200501080717/REVISED-FY21-25-Five-Year-Plan-Proposed.pdf"
        target="blank_"
      >revised budget proposal</a> as part of the City’s Five
      Year Financial Plan. The budget includes large spending cuts and declining
      tax revenues, reflecting the economic impact of the COVID-19 crisis. As
      part of an
      <a
        href="https://controller.phila.gov/philadelphia-audits/covid19-fiscal-impact/"
        target="blank_"
      >ongoing analysis</a> of the COVID-19 impact on City finances, the
      City Controller’s Office is releasing a tool to visualize and better
      understand the major changes in the newly released budget. The tool is
      intended to serve as a resource for policymakers and Philadelphians alike,
      bringing necessary transparency to the City’s budgeting process.
    </p>

    <p>
      With declining revenue sources, the City has been forced to make difficult
      choices to reduce spending. The Controller’s Office believes transparency
      is crucial to evaluating those choices. Ultimately, the City must devise a
      budget that maintains City services and demonstrates efficient and
      effective use of taxpayer money, particularly at a time of historic
      unemployment and unprecedented challenges for local businesses.
    </p>

    <p class="font-weight-bold">
      View the changes for
      <router-link to="/spending" class="text-link">budgeted spending</router-link>&nbsp;or
      <router-link to="/revenue" class="text-link">projected revenue</router-link>.
    </p>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  components: {}
};
</script>


