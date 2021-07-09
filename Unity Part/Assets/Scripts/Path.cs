using UnityEngine;

public class Path : MonoBehaviour
{
    PathSpawner pathSpawner;
    private void Start()
    {
        pathSpawner = GameObject.FindObjectOfType<PathSpawner>(); // This will return the first object matching the PathSpawner I only have one.
    }
    private void OnTriggerExit(Collider other)
    {
        //To check if what exited was the camera or not (but here only the cam is moving ,so no problem).
        if (other.gameObject.name=="MaleDummy")
        {
            pathSpawner.spawnObjects(); 
            if (CharacterMovement.afterBombMovement)//To avoid destroying it in the "losing effect".
            {
                pathSpawner.destroy_current_wall_clone();
                Destroy(gameObject, 2f); // Destroy after 2sec
            }
        }

    }

    // Update is called once per frame
    private void Update()
    {
        
    }
}
