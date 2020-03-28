import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import router from './router'
import store from './store'
import getPageTitle from './utils/getPageTitle'

NProgress.configure({ showSpinner: false }) // NProgress Configuration

router.beforeEach(async (to, from, next) => {
  // start progress bar
  NProgress.start()

  // set page title
  document.title = getPageTitle(to.meta.title)

  try {
    // init store data
    if (store.state.basedata.reportTypes.data.length === 0) {
      await store.dispatch('basedata/loadReportTypes')
      await store.dispatch('basedata/loadAccountingSubjects')
    }

    if (store.state.basedata.territories.data.length === 0) {
      await store.dispatch('basedata/loadTerritories', { omit: 'stocks' })
    }

    if (store.state.basedata.sections.data.length === 0) {
      await store.dispatch('basedata/loadSections', { omit: 'stocks' })
    }

    if (store.state.basedata.concepts.data.length === 0) {
      await store.dispatch('basedata/loadConcepts', { omit: 'stocks' })
    }

    if (store.state.basedata.industries.data.length === 0) {
      await store.dispatch('basedata/loadIndustries', { omit: 'stocks' })
    }
  } catch (error) {
    console.log(error)
    NProgress.done()
  }

  next()
})

router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})
