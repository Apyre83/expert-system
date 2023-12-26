# Pour chaque fichier dans $1, tester le fichier et attendre le retour de l'utilisateur pour passer au fichier suivant
for file in $1/*.txt; do
	clear
	echo "Test $file"
	python3.10 main.py $file

	echo ""
	echo ""
	echo "File:"
	cat $file

	read -p "Press enter to continue"
done
