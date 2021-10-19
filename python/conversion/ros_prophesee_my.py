import numpy as np
import rosbag
from data.format import Events
from tqdm import tqdm
import pdb

def get_events(bag_name):

    bag = rosbag.Bag(bag_name) 
    # make h5py file
    event_current_size = 1000000
    event_x = np.zeros(event_current_size, dtype=np.uint16)
    event_y = np.zeros(event_current_size, dtype=np.uint16)
    event_p = np.zeros(event_current_size, dtype=np.uint8)
    event_t = np.zeros(event_current_size, dtype=np.uint64)

    events_count = 0
    packet_count = 0
    # match the joint angles based on events
    for topic, msg, t in tqdm(bag.read_messages(topics=['/prophesee/camera/cd_events_buffer'])):
        if topic == "/prophesee/camera/cd_events_buffer":
            if events_count + len(msg.events) > event_current_size: 
                event_x.resize((event_current_size*2))
                event_y.resize((event_current_size*2))
                event_p.resize((event_current_size*2))
                event_t.resize((event_current_size*2))
                event_current_size *= 2

            for i in range(len(msg.events)):
                event = msg.events[i]
                tt = event.ts.to_nsec() // 1000
                polarity = int(event.polarity)

                event_x[events_count] = event.x
                event_y[events_count] = event.y
                event_p[events_count] = polarity
                event_t[events_count] = tt

                events_count += 1

            #events_dset[events_count: events_count + events.shape[0], :] = events
            #events_count += events.shape[0]
    pdb.set_trace()

    event_x.resize(events_count)
    event_y.resize(events_count)
    event_p.resize(events_count)
    event_t.resize(events_count)

    events = Events(
            np.asarray(event_x, dtype='uint16'),
            np.asarray(event_y, dtype='uint16'),
            np.asarray(event_p, dtype='uint8'),
            np.asarray(event_t, dtype='int64'))

    bag.close()

    return events
