using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CheckPoint : MonoBehaviour
{
    private TrackCheckpoints trackCp;
    private void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Vehicle" || other.tag == "AIVehicle")
        {
            trackCp.CarThroughCheckpoint(this, other.transform);
        }
    }

    public void SetTrackCheckpoints(TrackCheckpoints trackCp)
    {
        this.trackCp = trackCp;
    }
}
