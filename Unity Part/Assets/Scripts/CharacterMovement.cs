using UnityEngine;

public class CharacterMovement : MonoBehaviour
{
    public float speed = 65;
    public Rigidbody rigidBody;
    private static bool gameOverMode = false;
    public static bool afterBombMovement = true;
    private void Start()
    {
        gameOverMode = false;
        afterBombMovement = true;
    }
    private void FixedUpdate()
    {
        if (!gameOverMode)
        {
            Vector3 goForward = transform.forward * speed * Time.fixedDeltaTime;
            rigidBody.MovePosition(rigidBody.position + goForward);
        }
        else
        {
            if(afterBombMovement)
            {
                afterBombMovement = false;
                Vector3 goForward = transform.forward * speed *-1* Time.fixedDeltaTime;
                rigidBody.MovePosition(rigidBody.position + goForward);
            }
        }

    }

    public static void gameOver()
    {
        gameOverMode = true;
    }
}
