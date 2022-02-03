using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SmokeSystem : MonoBehaviour
{
    public GameObject smokePrefab;
    public CarController controller;
    [Range(0,0.5f)] public float slipLimit;

    public Transform[] wheelTransforms;
    public WheelCollider[] wheelColliders;
    public GameObject[] smokes;
    public ParticleSystem[] SmokeParticles;

    // Start is called before the first frame update
    void Start()
    {
        findValues();
    }

    void findValues(){
        controller = GetComponent<CarController>();
        wheelTransforms = controller.transforms;
        wheelColliders = controller.wheels;
        smokes = new GameObject[wheelTransforms.Length];
        SmokeParticles = new ParticleSystem[wheelTransforms.Length];
        smokePrefab = GameObject.Find("SkidSmoke");
    }

    private bool stupidFlag = false;

    void FixedUpdate(){
        if (stupidFlag == false) { spawnSmokes(); }
        if (stupidFlag == true) runSmokes();
    }
    
    void spawnSmokes(){
        if (wheelTransforms[3] == null) return;
        if (SmokeParticles == null) return;
        if (smokePrefab == null) return;
        for(int i = 0; i< wheelTransforms.Length; i++){
            smokes[i] = Instantiate(smokePrefab);
            SmokeParticles[i] = smokes[i].GetComponent<ParticleSystem>();
            smokes[i].transform.parent = wheelTransforms[i].transform;
            smokes[i].transform.position = wheelTransforms[i].transform.position;
            smokes[i].transform.rotation = Quaternion.identity;
            smokes[i].transform.localScale = new Vector3(1,1,1);
        }
        stupidFlag = true;
    }

    void runSmokes(){
        WheelHit hit;
        for (int i =0; i < wheelTransforms.Length; i++){
            if(wheelColliders[i].GetGroundHit(out hit)){
                if(Mathf.Abs(hit.forwardSlip) + Mathf.Abs(hit.sidewaysSlip)  >= slipLimit){
                    if(!SmokeParticles[i].isPlaying){
                        SmokeParticles[i].Play();
                    }
                }
                else{
                    if(!SmokeParticles[i].isStopped){
                        SmokeParticles[i].Stop();
                    }
                }
            }
        }
    }
}
