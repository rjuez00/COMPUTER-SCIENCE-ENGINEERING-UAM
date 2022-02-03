using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerCollisionDetection : MonoBehaviour
{

    void OnCollisionEnter(Collision collision)
    {
        string colTag = collision.gameObject.tag;
        if (colTag == "NPCPursuit" || colTag == "InvisibleBarrier")
        {
            Pursuit.Instance.EndPursuit();
        }

    }
}
