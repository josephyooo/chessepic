from py2exe import freeze
import epicengine
freeze(
    console=[r"c:\\Users\\Rameen Aziz\\Documents\\Experimental\\chessepic\\engine.py"],
    windows=[],
    data_files=None,
    zipfile=(r'c:\\Users\\Rameen Aziz\\Documents\\Experimental\\epic engine\\library.zip'),
    #options={}
    #version_info={3.11}
)