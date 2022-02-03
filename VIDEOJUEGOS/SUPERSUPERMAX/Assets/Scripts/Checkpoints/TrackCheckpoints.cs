using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Events;


public class TrackCheckpoints : MonoBehaviour
{
    private static TrackCheckpoints instance = null;

    public CheckPoint cpMeta;
    public List<CheckPoint> checkPoints; // Tienen que estar en orden, empezando por la meta

    public Text lapCountText;
    public int nLaps;

    // Function to call when the finish line is crossed by the player
    public UnityEvent invokeMethod;

    // List with all car transforms where the not AI car always has to be the first
    // Because the game will stop when the first car in the list finishes the race
    [SerializeField] private List<Transform> carTransforms;
    private List<CheckPoint> lastCheckpointList;

    // Time when each car crossed their last checkpoint
    private List<float> timeLastCheckpointList;

    // List with the lap count of each car
    private List<int> currentLaps;

    private List<int> finishOrder;
    private int _playerPosition;

    private int nCheckpoints;

    // When the player crosses the finish line we stop updating the position
    private bool stopUpdatingPos = false;

    private float time;

    private int _nCars;

    public static TrackCheckpoints Instance
    {
        get
        {
            if (instance == null)
            {
                instance = FindObjectOfType<TrackCheckpoints>();
                if (instance == null)
                {
                    instance = new GameObject("TrackCheckpoints").AddComponent<TrackCheckpoints>();
                }
            }
            return instance;
        }
    }

    private void Start()
    {
        time = 0.0f;

        foreach (CheckPoint cp in checkPoints)
        {
            cp.SetTrackCheckpoints(this);
        }

        lastCheckpointList = new List<CheckPoint>();
        timeLastCheckpointList = new List<float>();
        currentLaps = new List<int>();

        // Find the players car and 
        Transform playerCarTransform = GameObject.FindGameObjectWithTag("Vehicle").transform;
        lastCheckpointList.Add(checkPoints.Last());
        timeLastCheckpointList.Add(time);
        currentLaps.Add(0);

        // Same but for the ai cars
        foreach (Transform transf in carTransforms)
        {
            lastCheckpointList.Add(checkPoints.Last());
            timeLastCheckpointList.Add(time);
            currentLaps.Add(0);
        }

        // Inserts the player car at the start of the car list
        carTransforms.Insert(0, playerCarTransform);

        _nCars = currentLaps.Count;
        _playerPosition = _nCars;

        nCheckpoints = checkPoints.Count;

        finishOrder = new List<int>();
    }

    public void Update()
    {
        time += Time.deltaTime;
    }

    public void CarThroughCheckpoint(CheckPoint cp, Transform carTransform)
    {
        // int lastCheckpointIdx = checkPoints.IndexOf(lastVisited);
        int carIdx = carTransforms.IndexOf(carTransform);
        int lastCheckpointIdx = checkPoints.IndexOf(lastCheckpointList[carIdx]);
        int currCheckpointIdx = checkPoints.IndexOf(cp);

        lastCheckpointList[carIdx] = cp;
        timeLastCheckpointList[carIdx] = time;
        if (cp == cpMeta)
        {
            currentLaps[carIdx]++;
        }

        // Check if the last checkpoint visited (that counted) is the previous one
        if ( currCheckpointIdx == (lastCheckpointIdx + 1) % nCheckpoints )
        {

            // Update the position of the player each time any car crosses a checkpoint
            if (!stopUpdatingPos)
            {
                int playerLastCheckpoint = checkPoints.IndexOf(lastCheckpointList[0]);
                _playerPosition = 1;

                for (int aiCarIdx = 1; aiCarIdx < carTransforms.Count; aiCarIdx++)
                {

                    if (currentLaps[aiCarIdx] > currentLaps[0])
                    {
                        _playerPosition += 1;
                    }
                    else if (currentLaps[aiCarIdx] == currentLaps[0])
                    {
 
                        if (checkPoints.IndexOf(lastCheckpointList[aiCarIdx]) > playerLastCheckpoint)
                        {
                            _playerPosition += 1;
                        }
                        else if(checkPoints.IndexOf(lastCheckpointList[aiCarIdx]) == playerLastCheckpoint)
                        { 
                            if (timeLastCheckpointList[aiCarIdx] <= timeLastCheckpointList[0])
                            {
                                _playerPosition += 1;
                            }
                        }

                    }

                }

            }

            // Update lap counts and finish the game if the player crosses the finish
            // line in their last lap
            if (cp == cpMeta)
            {
                if ( currentLaps[carIdx] == nLaps + 1 )
                {
                    finishOrder.Add(carIdx);
                    if ( carIdx == 0)
                    {
                        _playerPosition = finishOrder.IndexOf(0) + 1;
                        // lapCountText.text = string.Empty;
                        stopUpdatingPos = true;
                        invokeMethod.Invoke();
                    }
                }
                else if (carIdx == 0)
                {
                    lapCountText.text = string.Format("Lap: {0}/{1}", currentLaps[carIdx], nLaps);
                }
                
            }

        }
 
    }

    public int PlayerPosition
    {
        get
        {
            return _playerPosition;
        }
    }

    public int NumberOfCars
    {
        get
        {
            return _nCars;
        }
    }

}
