from crapssim_api.tape import TapeWriter, TapeReader
from crapssim_api.session import Session


def test_tape_record_and_replay(tmp_path):
    tape_path = tmp_path/"run.tape"

    # Record
    writer = TapeWriter(str(tape_path))
    s = Session(record_callback=writer.write)
    s.start()
    s.step_roll(dice=[2,3])
    writer.close()

    # Replay
    read = list(TapeReader(str(tape_path)))
    assert read[1]["dice"] == [2,3]


