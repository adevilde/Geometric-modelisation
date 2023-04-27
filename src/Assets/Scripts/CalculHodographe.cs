using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CalculHodographe : MonoBehaviour
{
    // Nombre de subdivision dans l'algo de DCJ
    public int NombreDeSubdivision = 3;
    // Liste des points composant la courbe de l'hodographe
    private List<Vector3> ListePoints = new List<Vector3>();
    // Donnees i.e. points cliqués

    public GameObject Donnees;
    public GameObject particle;

    //////////////////////////////////////////////////////////////////////////
    // fonction : DeCasteljauSub                                            //
    // semantique : renvoie la liste des points composant la courbe         //
    //              approximante selon un nombre de subdivision données     //
    // params : - List<float> X : abscisses des point de controle           //
    //          - List<float> Y : odronnees des point de controle           //
    //          - int nombreDeSubdivision : nombre de subdivision           //
    // sortie :                                                             //
    //          - (List<float>, List<float>) : liste des abscisses et liste //
    //            des ordonnées des points composant la courbe              //
    //////////////////////////////////////////////////////////////////////////
    (List<float>, List<float>) DeCasteljauSub(List<float> X, List<float> Y, int nombreDeSubdivision)
    {
        // DeCasteljau algorithm recursive implementation

        List<float> XLgauche = new List<float>();
        List<float> YLgauche = new List<float>();

        List<float> XLdroite = new List<float>();
        List<float> YLdroite = new List<float>();

        List<float> XLTemp = new List<float>();
        List<float> YLTemp = new List<float>();
        
        int n = X.Count;

        if (nombreDeSubdivision <= 0) {
            return (X,Y);
        } else {
            // on ajoute Q0 à la liste gauche 
            XLgauche.Add(X[0]);
            YLgauche.Add(Y[0]);

            // on ajoute Rn-1 à la liste droite
            XLdroite.Add(X[n-1]);
            YLdroite.Add(Y[n-1]);

            // Calcul des points milieu
            for (int i = 0; i < n-1; ++i)
            {
                XLTemp.Add((X[i] + X[i+1]) / 2);
                YLTemp.Add((Y[i] + Y[i+1]) / 2);
            }

            // On ajoute Q1 à la liste gauche
            XLgauche.Add(XLTemp[0]);
            YLgauche.Add(YLTemp[0]);

            // On ajoute Rn-2 à la liste droite
            XLdroite.Add(XLTemp[XLTemp.Count-1]);
            YLdroite.Add(YLTemp[YLTemp.Count-1]);


            // Calcul des milieux des points de controle restants
            for (int i = 1; i < XLTemp.Count-1; ++i)
            {
                // Calcul des points milieu
                for (int j = 0; j < XLTemp.Count-i-1; ++j)
                {
                    XLTemp[j] = (XLTemp[j] + XLTemp[j+1]) / 2;
                    YLTemp[j] = (YLTemp[j] + YLTemp[j+1]) / 2;
                }
            

                // On ajoute Q1 à la liste gauche
                XLgauche.Add(XLTemp[0]);
                YLgauche.Add(YLTemp[0]);

                // On ajoute Rn-2 à la liste droite
                XLdroite.Add(XLTemp[XLTemp.Count-1-i]);
                YLdroite.Add(YLTemp[YLTemp.Count-1-i]);
            }
        }

        XLdroite.Reverse();
        YLdroite.Reverse();
        (XLgauche,YLgauche) = DeCasteljauSub(XLgauche, YLgauche, nombreDeSubdivision-1);
        (XLdroite,YLdroite) = DeCasteljauSub(XLdroite, YLdroite, nombreDeSubdivision-1);
        XLgauche.AddRange(XLdroite);
        YLgauche.AddRange(YLdroite);

        return (XLgauche, YLgauche);
    }

    //////////////////////////////////////////////////////////////////////////
    // fonction : Hodographe                                                //
    // semantique : renvoie la liste des vecteurs vitesses entre les paires //
    //              consécutives de points de controle                      //
    //              approximante selon un nombre de subdivision données     //
    // params : - List<float> X : abscisses des point de controle           //
    //          - List<float> Y : odronnees des point de controle           //
    //          - float Cx : offset d'affichage en x                        //
    //          - float Cy : offset d'affichage en y                        //
    // sortie :                                                             //
    //          - (List<float>, List<float>) : listes composantes des       //
    //            vecteurs vitesses sous la forme (Xs,Ys)                   //
    //////////////////////////////////////////////////////////////////////////
    (List<float>, List<float>) Hodographe(List<float> X, List<float> Y, float Cx = 1.5f, float Cy = 0.0f)
    {
        List<float> XSortie = new List<float>();
        List<float> YSortie = new List<float>();

        int n = X.Count; 
        for (int i=0; i < n-1 ; i++){
            XSortie.Add(n*(X[i+1] - X[i]));
            YSortie.Add(n*(Y[i+1] - Y[i]));
        }

        for (int i=0 ; i < YSortie.Count; i++) {
            for(int j=0; j < YSortie.Count - i -1; j++){
                YSortie[j] = (1 - Cy) * YSortie[j] + Cy * YSortie[j+1];
                XSortie[j] = (1 - Cx) * XSortie[j] + Cx * XSortie[j+1];
            }
        }
        
        return (XSortie, YSortie);
    }

    //////////////////////////////////////////////////////////////////////////
    //////////////////////////// NE PAS TOUCHER //////////////////////////////
    //////////////////////////////////////////////////////////////////////////
    void Start()
    {
        
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Return))
        {
            Instantiate(particle, new Vector3(1.5f, -4.0f, 0.0f), Quaternion.identity);
            var ListePointsCliques = GameObject.Find("Donnees").GetComponent<Points>();
            if (ListePointsCliques.X.Count > 0)
            {
                List<float> XSubdivision = new List<float>();
                List<float> YSubdivision = new List<float>();
                List<float> dX = new List<float>();
                List<float> dY = new List<float>();
                
                (dX, dY) = Hodographe(ListePointsCliques.X, ListePointsCliques.Y);

                (XSubdivision, YSubdivision) = DeCasteljauSub(dX, dY, NombreDeSubdivision);
                for (int i = 0; i < XSubdivision.Count; ++i)
                {
                    ListePoints.Add(new Vector3(XSubdivision[i], -4.0f, YSubdivision[i]));
                }
            }

        }
    }

    void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.blue;
        for (int i = 0; i < ListePoints.Count - 1; ++i)
        {
            Gizmos.DrawLine(ListePoints[i], ListePoints[i + 1]);
        }
    }
}
