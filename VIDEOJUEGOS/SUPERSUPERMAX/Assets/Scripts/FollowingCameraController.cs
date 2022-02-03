using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FollowingCameraController : MonoBehaviour
{
    public CarController RR;
    public Transform followedObject;
    public Vector3 offset;
    
    public float moveSpeed = 6.0f;
    public float rotSpeed = 20.0f;
    
        private void Start()
    {
  
    
        FindValues();
        defaultFOV = Camera.main.fieldOfView;
        desiredFOV = defaultFOV + 30;
    }


    void FindValues(){
        RR = GameObject.FindGameObjectWithTag("Vehicle").GetComponent<CarController>();
        followedObject = GameObject.FindGameObjectWithTag("Vehicle").transform;
    }

    public void MoveToTarget()
        {

            Vector3 targetPos = followedObject.position +
                                followedObject.forward * offset.z +
                                followedObject.right * offset.x +
                                followedObject.up * offset.y;
            transform.position = Vector3.Lerp(transform.position, targetPos, moveSpeed * Time.deltaTime);

        Vector3 focus = followedObject.gameObject.transform.position;
        Vector3 relativePos = focus - transform.position;
        Quaternion toRotation = Quaternion.LookRotation(relativePos);
        transform.rotation = Quaternion.Lerp(transform.rotation, toRotation, 1 * Time.deltaTime);


        //transform.LookAt(followedObject.gameObject.transform.position);

    }

    private void FixedUpdate()
    {
        MoveToTarget();
        boostFOV();
    }


    public float defaultFOV = 0, desiredFOV = 0;
    [Range(0, 50)] public float smoothTime = 2;
    private void boostFOV() { 
    
        if (RR.nitrusFlag)
        {
            Camera.main.fieldOfView = Mathf.Lerp(Camera.main.fieldOfView, desiredFOV, Time.deltaTime * 5);
        }
        else
        {
            Camera.main.fieldOfView = Mathf.Lerp(Camera.main.fieldOfView, defaultFOV, Time.deltaTime * 5);
        }
    }




}


