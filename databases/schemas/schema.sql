BEGIN TRANSACTION;


   CREATE TABLE players (
          user_id INTEGER PRIMARY KEY UNIQUE,
          level INTEGER NOT NULL DEFAULT 1,
          experience INTEGER NOT NULL DEFAULT 0,
          health INTEGER NOT NULL DEFAULT 100,
          gold INTEGER NOT NULL DEFAULT 0,
          class TEXT NOT NULL
          );


   CREATE TABLE inventories (
          inventory_id INTEGER PRIMARY KEY UNIQUE,
          /* Items */
          CONSTRAINT fk_inventory_id FOREIGN KEY (inventory_id) REFERENCES players (user_id) ON DELETE CASCADE
          );


   INSERT INTO players (user_id, class)
   VALUES (1, 'Warrior');


   INSERT INTO inventories (inventory_id)
   VALUES (1);


   INSERT INTO players (user_id, class)
   VALUES (2, 'Elf');


   INSERT INTO inventories (inventory_id)
   VALUES (2);


COMMIT TRANSACTION;