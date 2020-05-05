<template>
  <div class="home-page text-left ml-3 mr-3">
    <p>
      In response to declining tax revenues related to the COVID-19 pandemic,
      Mayor Kenney released a
      <a
        class="text-link"
        href="https://www.phila.gov/media/20200501080717/REVISED-FY21-25-Five-Year-Plan-Proposed.pdf"
        target="blank_"
      >revised budget proposal</a>
      as part of the City’s Five
      Year Financial Plan on May 1, 2020. Relative to the
      <a
        class="text-link"
        href="https://www.phila.gov/media/20200324135241/FYP-FullLayout-Final_ONLINE_3.23.pdf"
        target="blank_"
      >original March budget</a>,
      the new proposal includes large spending cuts, reflecting the economic
      impact of the COVID-19 crisis and the City’s response to it.
    </p>
    <p>
      As part of an
      <a
        class="text-link"
        href="https://controller.phila.gov/philadelphia-audits/covid19-fiscal-impact/"
        target="blank_"
      >ongoing analysis</a>
      of the COVID-19 impact on City finances, the City
      Controller’s Office is releasing a tool to visualize and better understand the
      major changes in the newly released budget. The tool is intended to serve as a
      resource for policymakers and Philadelphians alike, bringing necessary
      transparency to the City’s budgeting process.
    </p>

    <p>
      Ultimately, the goal of any city government is to provide vital services
      to residents through the efficient and effective use of taxpayer money. At
      a time of historic unemployment, declining tax revenues and unprecedented
      challenges for local businesses, striving to reach this goal through
      strategic budget decisions is more important than ever.
    </p>

    <p>
      The visualization includes data on planned spending and estimated revenue
      for the City's General Fund for fiscal years 2020 through 2025. Spending
      data can be broken down by fiscal year, City department, spending class,
      and spending category. Additionally, revenue data can be viewed by fiscal
      year and revenue source.
    </p>

    <p class="font-weight-bold">
      View the changes for
      <router-link to="/spending" class="text-link">budgeted spending</router-link>&nbsp;or
      <router-link to="/revenue" class="text-link">projected revenue</router-link>.
    </p>

    <div class="footnotes">
      <h3>Sources</h3>
      <hr class="titlebar" />
      <p>
        All data is taken directly from City budget documents. The
        visualization shows the difference between the revised Five Year Plan,
        as released May 1, and the original proposal from March 5.
        These budget documents can be found
        <a
          class="text-link"
          href="https://www.phila.gov/documents/mayor-kenneys-fiscal-year-2021-budget/"
          target="blank_"
        >here</a>.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  components: {}
};
</script>


<style>
.footnotes {
  margin-top: 100px;
}
</style>


