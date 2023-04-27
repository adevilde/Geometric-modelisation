using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

//////////////////////////////////////////////////////////////////////////
///////////////// Classe qui gère la subdivision via DCJ /////////////////
//////////////////////////////////////////////////////////////////////////
public class DeCasteljauSubdivision : MonoBehaviour
{
    // Pas d'échantillonage pour affichage
    public float pas = 1 / 100;
    // Nombre de subdivision dans l'algo de DCJ
    public int NombreDeSubdivision = 3;
    // Liste des points composant la courbe
    private List<Vector3> ListePoints = new List<Vector3>();
    // Donnees i.e. points cliqués
    public GameObject Donnees;
    // Coordonnees des points composant le polygone de controle
    private List<float> PolygoneControleX = new List<float>();
    private List<float> PolygoneControleY = new List<float>();

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
    //////////////////////////// NE PAS TOUCHER //////////////////////////////
    //////////////////////////////////////////////////////////////////////////
    void Start()
    {

    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Return))
        {
            var ListePointsCliques = GameObject.Find("Donnees").GetComponent<Points>();
            if (ListePointsCliques.X.Count > 0)
            {
                for (int i = 0; i < ListePointsCliques.X.Count; ++i)
                {
                    PolygoneControleX.Add(ListePointsCliques.X[i]);
                    PolygoneControleY.Add(ListePointsCliques.Y[i]);
                }
                List<float> XSubdivision = new List<float>();
                List<float> YSubdivision = new List<float>();

                (XSubdivision, YSubdivision) = DeCasteljauSub(ListePointsCliques.X, ListePointsCliques.Y, NombreDeSubdivision);
                for (int i = 0; i < XSubdivision.Count; ++i)
                {
                    ListePoints.Add(new Vector3(XSubdivision[i], -4.0f, YSubdivision[i]));
                }
            }

        }
    }

    void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.red;
        for (int i = 0; i < PolygoneControleX.Count - 1; ++i)
        {
            Gizmos.DrawLine(new Vector3(PolygoneControleX[i], -4.0f, PolygoneControleY[i]), new Vector3(PolygoneControleX[i + 1], -4.0f, PolygoneControleY[i + 1]));
        }

        Gizmos.color = Color.blue;
        for (int i = 0; i < ListePoints.Count - 1; ++i)
        {
            Gizmos.DrawLine(ListePoints[i], ListePoints[i + 1]);
        }
    }
}
