"""
python -m orchard.projects.v1.tools.shell
"""

import apsw.shell
import orchard.projects.v1.models.engine

if __name__ == "__main__":
    orchard.projects.v1.models.engine.setup_db()
    shell = apsw.shell.Shell(db=orchard.projects.v1.models.engine.engine)
    shell.process_command(".mode line")
    shell.cmdloop()