using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarExplodeOnCollision : MonoBehaviour
{
    public GameObject explosionEffect;

    void OnCollisionEnter(Collision collision)
    {
        string colTag = collision.gameObject.tag;
        if (colTag == "NPCPursuit" || colTag == "Vehicle" || colTag == "InvisibleBarrier")
        {
            Instantiate(explosionEffect, transform.position, transform.rotation);
            Destroy(gameObject);
        }
        
    }
}
