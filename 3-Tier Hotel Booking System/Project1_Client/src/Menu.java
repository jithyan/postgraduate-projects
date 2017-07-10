import java.io.BufferedReader;

public abstract class Menu extends RootMenu {
   /* The menu that came before the current menu */
   private RootMenu previousMenu;


   public Menu(BufferedReader br, ClientHopp hopp, RootMenu previous) {
      super(br, hopp);
      this.previousMenu = previous;
   }


   public RootMenu getPrevious() {
      return previousMenu;
   }


   public void setPrevious(Menu previous) {
      this.previousMenu = previous;
   }
}
