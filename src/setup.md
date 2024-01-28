1. run `poetry install` in src/backend
2. build fts extension, see instructions in `src/backend/orchard/libs/signal_fts5`
3. optionally seed with the test data python -m orchard.projects.v1.tools.generate_test_data
3. run `npm install` in src/frontend
4. install procfile manager, I use "Hivemind" https://github.com/DarthSim/hivemind
5. run the Procfile