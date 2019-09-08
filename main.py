import app.loader
import app.router
import app.ui

loader = app.loader.CSVLoader()
router = app.router.Router()
ui = app.ui.CommandLineUI(loader=loader, router=router)
ui.start()
